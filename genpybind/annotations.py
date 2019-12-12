# -*- coding: utf-8; -*-

import ast
import collections

from clang.cindex import CursorKind

from . import utils

if False:  # pylint: disable=using-constant-test
    from .decls.declarations import Declaration  # pylint: disable=unused-import
    from clang import cindex  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        cast, Any, Container, Iterable, List, Optional, Text, Tuple, Type, Union)
    AnnotationArgumentT = Union[int, float, Text, bool, None]  # pylint: disable=invalid-name
    AnnotationT = Tuple[Text, Tuple[AnnotationArgumentT, ...]]  # pylint: disable=invalid-name
else:
    Text = None  # type: ignore # pylint: disable=invalid-name
    cast = lambda _, x: x  # type: ignore # pylint: disable=invalid-name


LOZENGE = "◊"
SPECIAL_NAMES = {"true": True, "false": False, "default": None, "none": None}


class Annotations(collections.Sequence):
    def __init__(self, annotations=None):
        # type: (Union[None, Text, Iterable[Text]]) -> None
        self._annotations = []  # type: List[AnnotationT]
        if isinstance(annotations, str):
            self.parse(cast(Text, annotations))
            return
        if annotations is None:
            return
        for annotation in annotations:
            self.parse(annotation)

    def __len__(self):
        # type: () -> int
        return len(self._annotations)

    def __getitem__(self, index):
        # type: (Any) -> AnnotationT
        # FIXME: should be (int) -> AnnotationT
        return self._annotations[index]  # type: ignore

    def extend(self, other):
        # type: (Annotations) -> None
        assert isinstance(other, Annotations)
        self._annotations.extend(other._annotations) # pylint: disable=protected-access

    def parse(self, annotation):
        # type: (Text) -> None
        if not annotation:
            return

        def append(key, arguments):
            # type: (Text, Iterable[AnnotationArgumentT]) -> None
            self._annotations.append((key, tuple(arguments)))

        def recurse_ast(elem):
            # type: (ast.AST) -> None
            if isinstance(elem, ast.Module):
                for module_elem in elem.body:
                    recurse_ast(module_elem)
                return None
            if isinstance(elem, ast.Expr):
                return recurse_ast(elem.value)
            if isinstance(elem, ast.Tuple):
                for tuple_elem in elem.elts:
                    recurse_ast(tuple_elem)
                return None
            if isinstance(elem, ast.Name):
                return append(elem.id, [])
            if isinstance(elem, ast.Call):
                arguments = []
                if any(getattr(elem, attr, None)
                       for attr in ["keywords", "kwargs", "starargs"]):
                    raise RuntimeError(
                        "star args and keyword arguments are not supported "
                        "in {!r}".format(annotation))
                for arg in elem.args:
                    value = None  # type: AnnotationArgumentT
                    if isinstance(arg, ast.Num):
                        value = arg.n
                    elif isinstance(arg, ast.Str):
                        value = arg.s
                    elif isinstance(arg, ast.Name):
                        value = SPECIAL_NAMES.get(arg.id.lower(), arg.id)
                    elif isinstance(arg, ast.NameConstant):
                        # "True", "False", "None" in Python 3
                        value = arg.value
                    else:
                        raise RuntimeError(
                            "unknown argument type {!r} in {!r}".format(arg, annotation))
                    arguments.append(value)
                return append(elem.func.id, arguments)  # type: ignore
            raise RuntimeError(
                "unknown AST element {!r} in {!r}".format(elem, annotation))

        module = ast.parse(annotation)
        recurse_ast(module)

    @classmethod
    def from_cursor(cls, cursor):
        # type: (cindex.Cursor) -> Annotations
        annotations = []
        for child in cursor.get_children(
                with_implicit=True, with_template_instantiations=True):
            if child.kind != CursorKind.ANNOTATE_ATTR:
                continue
            # TODO: .displayname or .spelling ? does it matter?
            text = child.spelling
            assert isinstance(text, str)
            if not text.startswith(LOZENGE):
                continue
            text = text[len(LOZENGE):]
            annotations.append(text)
        return cls(annotations)

    def apply_to(self, declaration, quiet=False, exclude=None):
        # type: (Declaration, bool, Optional[Container[Text]]) -> None
        for name, args in self._annotations:
            if exclude is not None and name in exclude:
                continue
            fun = getattr(declaration, "set_{}".format(name), None)
            if callable(fun):
                pass
            elif (callable(getattr(declaration, "set", None)) and
                  declaration.set(name, *args)):  # type: ignore
                continue
            elif not quiet:
                raise RuntimeError(
                    "{} does not support {!r} annotation".format(
                        declaration.__class__.__name__, name))
            fun(*args)

    def __repr__(self):  # type: ignore
        # type: () -> Text
        return ", ".join([
            "{}({})".format(name, ", ".join(map(repr, args)))
            for name, args in self._annotations
        ])
