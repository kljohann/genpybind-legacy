from __future__ import unicode_literals
import sys

from clang.cindex import CursorKind

from .. import cutils, utils
from ..utils import join_arguments, quote
from .callables import Callable, METHOD_KINDS

if False:  # pylint: disable=using-constant-test
    from clang import cindex  # pylint: disable=unused-import
    from ..annotations import Annotations  # pylint: disable=unused-import
    from .declarations import Declaration  # pylint: disable=unused-import
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        Any, Iterable, List, Optional, Text, Tuple, Type, Union)


_RAW_OPERATORS = [
    (("sub", "rsub"), "operator-", "l - r"),
    (("add", "radd"), "operator+", "l + r"),
    (("mul", "rmul"), "operator*", "l * r"),
    (("mod", "rmod"), "operator%", "l % r"),
    (("lshift", "rlshift"), "operator<<", "l << r"),
    (("rshift", "rrshift"), "operator>>", "l >> r"),
    (("and", "rand"), "operator&", "l & r"),
    (("or", "ror"), "operator|", "l | r"),
    (("xor", "rxor"), "operator^", "l ^ r"),
    (("eq", "eq"), "operator==", "l == r"),
    (("ne", "ne"), "operator!=", "l != r"),
    (("gt", "lt"), "operator>", "l > r"),
    (("ge", "le"), "operator>=", "l >= r"),
    (("lt", "gt"), "operator<", "l < r"),
    (("le", "ge"), "operator<=", "l <= r"),
    (("iadd",), "operator+=", "l += r"),
    (("isub",), "operator-=", "l -= r"),
    (("imul",), "operator*=", "l *= r"),
    (("imod",), "operator%=", "l %= r"),
    (("ilshift",), "operator<<=", "l <<= r"),
    (("irshift",), "operator>>=", "l >>= r"),
    (("iand",), "operator&=", "l &= r"),
    (("ior",), "operator|=", "l |= r"),
    (("ixor",), "operator^=", "l ^= r"),
    (("neg",), "operator-", "-l"),
    (("pos",), "operator+", "+l"),
    (("invert",), "operator~", "(~l)"),
]  # type: List[Tuple[Tuple[Text, ...], Text, Text]]

_RAW_OPERATORS.extend([
    ((("truediv", "rtruediv"), "operator/", "l / r") if sys.version_info >= (3,)
     else (("div", "rdiv"), "operator/", "l / r")),
    ((("itruediv",), "operator/=", "l /= r") if sys.version_info >= (3,)
     else (("idiv",), "operator/=", "l /= r")),
])

_OPERATORS = {
    (key, 1 + expr.count("r")):(names, expr)
    for (names, key, expr) in _RAW_OPERATORS
}


class Operator(Callable):
    __slots__ = (
        "_friend_cursor",
        "_stringstream",
    )

    @classmethod
    def or_else(cls, other_cls):
        # type: (Type[Declaration], Optional[Type[Declaration]]) -> Any
        def wrapper(cursor, annotations=None, **kwargs):
            # type: (cindex.Cursor, Optional[Annotations], **Any) -> Optional[Declaration]
            assert annotations is not None
            declaration = (other_cls or cls)(cursor, **kwargs)
            annotations.apply_to(declaration, quiet=True)
            expose_as = declaration.expose_as
            if expose_as.startswith("operator") and not expose_as == "operator()":
                if declaration.implicit:
                    # Skip implicit move or copy assignment operators
                    return None
                return cls(cursor, **kwargs)
            if other_cls is not None:
                return other_cls(cursor, **kwargs)
            return None
        return wrapper

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(Operator, self).__init__(*args, **kwargs)
        self._friend_cursor = None  # type: Optional[cindex.Cursor]
        self._stringstream = None  # type: Optional[Tuple[Text, ...]]
        if self._cursor.kind == CursorKind.FRIEND_DECL:
            child = next(self._cursor.get_children(
                with_implicit=True, with_template_instantiations=True), None)
            if child is None:
                return
            self._friend_cursor = self._cursor
            self._cursor = child

    @property
    def friend_cursor(self):
        # type: () -> Optional[cindex.Cursor]
        return self._friend_cursor

    @property
    def stringstream(self):
        # type: () -> Optional[Tuple[Text, ...]]
        if self._stringstream is None:
            return None
        return tuple(self._stringstream)

    def set_stringstream(self, *expose_as):
        # type: (*Text) -> None
        if self.spelling not in ["operator<<", "operator>>"]:
            raise RuntimeError(
                "stringstream annotation not supported for {}".format(self))
        self._stringstream = expose_as

    @property
    def fully_qualified_name(self):
        # type: () -> Text
        if self.friend_cursor is None:
            return super(Operator, self).fully_qualified_name
        return cutils.fully_qualified_name(self.cursor)

    def _record_type(self):
        # type: () -> cindex.Type
        return self.parent_cursor.type

    def _argument_types(self):
        # type: () -> List[cindex.Type]
        argument_types = []

        if self.friend_cursor is None:
            assert self.cursor.kind in METHOD_KINDS
            argument_types.append(self._record_type())

        for type_ in self.cursor.type.argument_types():
            if cutils.is_valid_type(type_.get_pointee()):
                type_ = type_.get_pointee()
            # TODO: Retrieve non-const-qualified type
            argument_types.append(type_)

        return argument_types

    def expose_stringstream(self, parent, _registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        assert self.stringstream is not None
        assert self.spelling in ["operator<<", "operator>>"]
        if self.spelling == "operator>>":
            yield "// FIXME: expose {}".format(self)
            return
        expose_as = self.stringstream or ["__str__", "__repr__"]
        for name in expose_as:
            yield "{parent}.def({args});".format(
                parent=parent,
                args=join_arguments(
                    quote(name),
                    "genpybind_stringstream_helper<{}>()".format(
                        self._record_type().fully_qualified_name),
                )
            )

    def statements(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        assert self.spelling.startswith("operator")
        assert not self.implicit

        if self.spelling == "operator=":
            return

        if self.stringstream is not None:
            for result in self.expose_stringstream(parent, registry):
                yield result
            return

        argument_types = self._argument_types()

        key = (self.spelling, len(argument_types))
        operator = _OPERATORS.get(key, None)

        def unhandled(what=""):
            # type: (Text) -> Text
            return (
                "// FIXME: expose {}{}{}\n".format(what, " " if what else "", self) +
                "//        {} -> {}\n".format(key, operator) +
                "//        {}".format(
                    [t.fully_qualified_name for t in argument_types]))

        if not operator:
            yield unhandled("(conversion?)")
            return

        if not cutils.is_same_type(argument_types[0], self._record_type()):
            yield unhandled()
            return

        names, expr = operator  # type: Tuple[Text, ...], Text
        _typedef_name = registry.register(self.cursor, self)

        # TODO: Add support for call policies
        # TODO: Handle "r" variant of operators

        argument_types = self._argument_types()

        yield "{parent}.def({args});".format(
            parent=parent,
            args=join_arguments(
                quote("__{}__".format(names[0])),
                "[]({args}) {{ return {expr}; }}".format(
                    args=join_arguments(
                        "{} {}& {}".format(
                            utils.strip_prefix(tp.fully_qualified_name, "const "),
                            "const" if self.cursor.is_const_method() else "",
                            var)
                        for tp, var in zip(argument_types, ["l", "r"])),
                    expr=expr,
                ),
                quote(self.cursor.brief_comment),
                "py::is_operator()",
            )
        )
