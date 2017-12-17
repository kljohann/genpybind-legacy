from __future__ import unicode_literals

from clang.cindex import CursorKind

from .. import cutils
from ..utils import quote
from .declarations import Declaration

if False:  # pylint: disable=using-constant-test
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        Any, Dict, FrozenSet, Iterable, List, Optional, Set, Text, Tuple, Union)


class FieldOrVar(Declaration):
    __slots__ = (
        "_writable",
    )

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(FieldOrVar, self).__init__(*args, **kwargs)
        self._writable = True

    @property
    def writable(self):
        # type: () -> bool
        if self.is_field_or_static() and self.cursor.type.is_const_qualified():
            return False
        return self._writable

    def set_writable(self, value=True):
        # type: (bool) -> None
        if not self.is_field_or_static() and not value:
            raise RuntimeError(
                "'readonly' annotation not supported for {}".format(self))
        self._writable = bool(value)

    def set_readonly(self, value=True):
        # type: (bool) -> None
        self.set_writable(not value)

    def is_field_or_static(self):
        # type: () -> bool
        return cutils.first_parent_by_kind(
            self.cursor, [CursorKind.CLASS_DECL, CursorKind.STRUCT_DECL]) is not None

    def statements(self, parent, _registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if self.is_field_or_static():
            qualifier = "readwrite" if self.writable else "readonly"
            if self.cursor.kind == CursorKind.VAR_DECL:
                qualifier = "{}_static".format(qualifier)
            yield "{parent}.def_{qualifier}({name}, &{field});".format(
                qualifier=qualifier,
                field=self.fully_qualified_name,
                parent=parent,
                name=quote(self.expose_as),
            )
            return

        yield "{parent}.attr({name}) = {var};".format(
            parent=parent,
            name=quote(self.expose_as),
            var=self.fully_qualified_name,
        )
