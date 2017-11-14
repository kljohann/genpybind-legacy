# -*- coding: utf-8; -*-

from __future__ import unicode_literals

import ast
import collections

from clang.cindex import CursorKind


LOZENGE = u"◊"
SPECIAL_NAMES = {"true": True, "false": False, "default": None}


class Annotations(collections.Sequence):
    """
    >>> def as_list(inp): return list(Annotations(inp))
    >>> as_list("plain, call(), with_arg(some_name), with_args(a, b, c, 1, 2, 3, 'hello', \\"world\\")")
    [('plain', ()), ('call', ()), ('with_arg', ('some_name',)), ('with_args', ('a', 'b', 'c', 1, 2, 3, 'hello', 'world'))]
    >>> as_list("plain")
    [('plain', ())]
    >>> as_list(["multiple", "attributes(are, supported)"])
    [('multiple', ()), ('attributes', ('are', 'supported'))]
    >>> as_list("required(true), visible(False)")
    [('required', (True,)), ('visible', (False,))]
    """
    def __init__(self, annotations=None):
        self._annotations = []
        if not isinstance(annotations, list):
            annotations = [annotations]
        for annotation in annotations:
            self.parse(annotation)

    def __len__(self):
        return len(self._annotations)

    def __getitem__(self, index):
        return self._annotations[index]

    def extend(self, other):
        assert isinstance(other, Annotations)
        self._annotations.extend(other._annotations) # pylint: disable=protected-access

    def parse(self, annotation):
        if not annotation:
            return

        def append(key, arguments):
            self._annotations.append((key, tuple(arguments)))

        def recurse_ast(elem):
            if isinstance(elem, ast.Module):
                for elem_ in elem.body:
                    recurse_ast(elem_)
            elif isinstance(elem, ast.Expr):
                recurse_ast(elem.value)
            elif isinstance(elem, ast.Tuple):
                for elem_ in elem.elts:
                    recurse_ast(elem_)
            elif isinstance(elem, ast.Name):
                append(elem.id, [])
            elif isinstance(elem, ast.Call):
                arguments = []
                if any(getattr(elem, attr, None)
                       for attr in ["keywords", "kwargs", "starargs"]):
                    raise RuntimeError(
                        "star args and keyword arguments are not supported "
                        "in {!r}".format(annotation))
                for arg in elem.args:
                    if isinstance(arg, ast.Num):
                        arg = arg.n
                    elif isinstance(arg, ast.Str):
                        arg = arg.s
                    elif isinstance(arg, ast.Name):
                        arg = SPECIAL_NAMES.get(arg.id.lower(), arg.id)
                    else:
                        raise RuntimeError(
                            "unknown argument type {!r} in {!r}".format(arg, annotation))
                    arguments.append(arg)
                append(elem.func.id, arguments)
            else:
                raise RuntimeError(
                    "unknown AST element {!r} in {!r}".format(elem, annotation))

        module = ast.parse(annotation)
        recurse_ast(module)

    @classmethod
    def from_cursor(cls, cursor):
        annotations = []
        for child in cursor.get_children(
                with_implicit=True, with_template_instantiations=True):
            if child.kind != CursorKind.ANNOTATE_ATTR:
                continue
            # TODO: .displayname or .spelling ? does it matter?
            text = child.spelling
            try:
                string_type = unicode # Python 2
            except NameError:
                string_type = str # Python 3
            if not isinstance(text, string_type):
                text = text.decode("utf-8")
            if not text.startswith(LOZENGE):
                continue
            text = text[len(LOZENGE):]
            annotations.append(text)
        return cls(annotations)

    def apply_to(self, declaration, quiet=False, exclude=None):
        for name, args in self._annotations:
            if exclude is not None and name in exclude:
                continue
            fun = getattr(declaration, "set_{}".format(name), None)
            if callable(fun):
                pass
            elif (callable(getattr(declaration, "set", None)) and
                  declaration.set(name, *args)):
                continue
            elif not quiet:
                raise RuntimeError(
                    "{} does not support {!r} annotation".format(
                        declaration.__class__.__name__, name))
            fun(*args)

    def __repr__(self):
        return ", ".join([
            "{}({})".format(name, ", ".join(map(repr, args)))
            for name, args in self._annotations
        ])
