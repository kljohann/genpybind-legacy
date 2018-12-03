from __future__ import unicode_literals

from clang.cindex import Cursor, CursorKind

from .. import cutils, utils
from ..utils import join_arguments, quote
from .declarations import Declaration

if False:  # pylint: disable=using-constant-test
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import Any, Iterable, List, Optional, Text, Tuple, Union  # pylint: disable=unused-import


METHOD_KINDS = frozenset([
    CursorKind.CONVERSION_FUNCTION,
    CursorKind.CXX_METHOD,
])


class Callable(Declaration):
    __slots__ = (
        "_keep_alive",
        "_noconvert",
        "_required",
        "_return_value_policy",
    )

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(Callable, self).__init__(*args, **kwargs)
        self._return_value_policy = None  # type: Optional[Text]
        self._keep_alive = self._noconvert = self._required = ()  # type: Union[Tuple[()], List[int]]

    def _argument_index(self, value, prefix=None):
        # type: (Union[int, Text], Optional[List[Text]]) -> int
        arguments = []
        candidates = list(prefix or [])  # type: List[Union[Text, Cursor]]
        candidates.extend(self.cursor.get_arguments())
        for idx, elem in enumerate(candidates):
            if isinstance(elem, Cursor):
                assert elem.kind == CursorKind.PARM_DECL
                elem = elem.spelling
            if value in [elem, idx]:
                return idx
            arguments.append(elem)

        raise RuntimeError(
            "{!r} was given invalid argument specifier {!r}, expected one of {!r}".format(
                self, value, arguments))

    @property
    def return_value_policy(self):
        # type: () -> Optional[Text]
        return self._return_value_policy

    def set_return_value_policy(self, value):
        # type: (Optional[Text]) -> None
        self._return_value_policy = value

    @property
    def keep_alive(self):
        # type: () -> Tuple[int, ...]
        return tuple(self._keep_alive)

    def set_keep_alive(self, *values):
        # type: (*Union[int, str]) -> None
        prefix = ["return", "this"]  # [return value, self reference, arguments...]
        self._keep_alive = [
            self._argument_index(value, prefix=prefix) for value in values
        ]

    @property
    def noconvert(self):
        # type: () -> Tuple[int, ...]
        return tuple(self._noconvert)

    def set_noconvert(self, *values):
        # type: (*Union[int, str]) -> None
        self._noconvert = [self._argument_index(val) for val in values]

    @property
    def required(self):
        # type: () -> Tuple[int, ...]
        return tuple(self._required)

    def set_required(self, *values):
        # type: (*Union[int, str]) -> None
        self._required = [self._argument_index(val) for val in values]

    def argument_types(self):
        # type: () -> List[Text]
        return [tp.fully_qualified_name for tp in self.cursor.type.argument_types()]

    def typedef(self, name):
        # type: (Text) -> Text
        qualifiers = []
        namespace = ""
        if self.cursor.kind in METHOD_KINDS and not self.cursor.is_static_method():
            if self.cursor.is_const_method():
                qualifiers.append("const")
            namespace = "{}::".format(cutils.fully_qualified_name(self.parent_cursor))

        return "typedef {ret} ({namespace}*{name}) ({arguments}){qualifiers};".format(
            name=name,
            ret=self.cursor.type.get_result().fully_qualified_name,
            arguments=join_arguments(self.argument_types()),
            namespace=namespace,
            qualifiers=" " + (" ".join(qualifiers)) if qualifiers else "",
        )

    def policies(self):
        # type: () -> Iterable[Text]
        if self.return_value_policy:
            yield "py::return_value_policy::{}".format(self.return_value_policy)
        if self.keep_alive:
            yield "py::keep_alive<{}>()".format(", ".join(str(idx) for idx in self.keep_alive))

    def function_pointer(self, cast_type=None):
        # type: (Optional[Text]) -> Text
        return "{cast}&{field}".format(
            cast="({})".format(cast_type) if cast_type is not None else "",
            field=self.fully_qualified_name,
        )

    def function_object(self, cast_type=None):
        # type: (Optional[Text]) -> Text
        return "py::cpp_function({})".format(
            join_arguments(
                self.function_pointer(cast_type),
                self.policies(),
            )
        )

    def arguments(self):
        # type: () -> List[Text]
        args = []
        is_after_args_or_kwargs = False
        for idx, child in enumerate(
                cutils.children_by_kind(self.cursor, CursorKind.PARM_DECL)):
            # according to pybind11 docs do not use pybind11::arg for pybind11::{args,kwargs} types
            if child.type.fully_qualified_name in ['::pybind11::args', '::pybind11::kwargs']:
                is_after_args_or_kwargs = True
                continue
            if is_after_args_or_kwargs:
                 raise RuntimeError("py::args / py::kwargs cannot be followed by other arguments")
            default_value = ""
            expr = next(cutils.children_by_kind(child, cutils.EXPRESSION_KINDS), None)
            if expr:
                default_value = cutils.fully_qualified_expression(expr)
                # FIXME: expression sometimes includes leading "=", see
                # https://reviews.llvm.org/D33644
                default_value = " = {}".format(utils.strip_prefix(default_value, "="))
            args.append("py::arg({name}){noconvert}{required}{value}".format(
                name=quote(child.spelling),
                noconvert=".noconvert()" if idx in self.noconvert else "",
                required=".none(false)" if idx in self.required else "",
                value=default_value,
            ))
        return args

    def statements(self, parent, _registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        typedef_name = "genpybind_{}_type".format(self.expose_as)

        yield "{"
        yield self.typedef(typedef_name)
        yield "{parent}.def{qualifier}({args});".format(
            parent=parent,
            qualifier="_static" if self.cursor.is_static_method() else "",
            args=join_arguments(
                quote(self.expose_as),
                self.function_pointer(typedef_name),
                quote(self.cursor.brief_comment),
                self.arguments(),
                self.policies(),
            )
        )
        yield "}"


class Function(Callable):
    def set_stringstream(self, *args):
        # type: (*Any) -> None
        # As annotations can not be attached to a friend declaration, we need to
        # ignore annotations applicable to operator friend declarations here.
        pass
