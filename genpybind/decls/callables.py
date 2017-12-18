from __future__ import unicode_literals

import re

from clang.cindex import CursorKind

from .. import cutils, utils
from ..utils import join_arguments, quote
from .declarations import Declaration


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
        super(Callable, self).__init__(*args, **kwargs)
        self._return_value_policy = None
        self._keep_alive = self._noconvert = self._required = tuple()

    def _argument_index(self, value, prefix=None):
        arguments = (prefix or []) + list(self.cursor.get_arguments())
        for index, elem in enumerate(arguments):
            if elem is not None and not isinstance(elem, basestring):
                assert elem.kind == CursorKind.PARM_DECL
                elem = elem.spelling
            if elem == value:
                return index

        if isinstance(value, int) and value <= index:
            return value

        raise RuntimeError(
            "{!r} was given invalid argument specifier {!r}".format(
                self, value))

    @property
    def return_value_policy(self):
        return self._return_value_policy

    def set_return_value_policy(self, value):
        self._return_value_policy = value

    @property
    def keep_alive(self):
        return tuple(self._keep_alive)

    def set_keep_alive(self, *values):
        # [return value, self reference, arguments...]
        prefix = ["return", "this"]
        self._keep_alive = [
            self._argument_index(value, prefix=prefix) for value in values
        ]

    @property
    def noconvert(self):
        return tuple(self._noconvert)

    def set_noconvert(self, *values):
        self._noconvert = [self._argument_index(val) for val in values]

    @property
    def required(self):
        return tuple(self._required)

    def set_required(self, *values):
        self._required = [self._argument_index(val) for val in values]

    def argument_types(self):
        return [tp.fully_qualified_name for tp in self.cursor.type.argument_types()]

    def typedef(self, name):
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
        return [
            ("py::return_value_policy::{}".format(self.return_value_policy)
             if self.return_value_policy else None),
            ("py::keep_alive<{}>()".format(", ".join(str(idx) for idx in self.keep_alive))
             if self.keep_alive else None),
        ]

    def function_pointer(self, cast_type=None):
        return "{cast}&{field}".format(
            cast="({})".format(cast_type) if cast_type is not None else "",
            field=self.fully_qualified_name,
        )

    def function_object(self, cast_type=None):
        return "py::cpp_function({})".format(
            join_arguments(
                self.function_pointer(cast_type),
                self.policies(),
            )
        )

    def arguments(self):
        args = []
        for ii, child in enumerate(
                cutils.children_by_kind(self.cursor, CursorKind.PARM_DECL)):
            default_value = ""
            expr = next(cutils.children_by_kind(child, cutils.EXPRESSION_KINDS), None)
            if expr:
                default_value = cutils.fully_qualified_expression(expr)
                # FIXME: expression sometimes includes leading "=", see
                # https://reviews.llvm.org/D33644
                default_value = " = {}".format(utils.strip_prefix(default_value, "="))
            args.append("py::arg({name}){noconvert}{required}{value}".format(
                name=quote(child.spelling),
                noconvert=".noconvert()" if ii in self.noconvert else "",
                required=".none(false)" if ii in self.required else "",
                value=default_value,
            ))
        return args

    def statements(self, parent, registry):
        typedef_name = registry.register(self.cursor, self)

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


class Function(Callable):
    def set_stringstream(self, *args):
        # As annotations can not be attached to a friend declaration, we need to
        # ignore annotations applicable to operator friend declarations here.
        pass
