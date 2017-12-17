from __future__ import unicode_literals

from clang.cindex import CursorKind

from .. import cutils
from .declarations import Declaration
from ..utils import join_arguments, quote

if False:  # pylint: disable=using-constant-test
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import Any, Iterable, Optional, Text, Tuple, Union  # pylint: disable=unused-import


class Enum(Declaration):
    __slots__ = (
        "_arithmetic",
        "_export_values",
    )

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(Enum, self).__init__(*args, **kwargs)
        self._arithmetic = False
        self._export_values = None  # type: Optional[bool]

    @property
    def arithmetic(self):
        # type: () -> bool
        return self._arithmetic

    def set_arithmetic(self, value=True):
        # type: (bool) -> None
        self._arithmetic = bool(value)

    @property
    def export_values(self):
        # type: () -> Optional[bool]
        return self._export_values

    def set_export_values(self, value=True):
        # type: (Optional[bool]) -> None
        if value not in [True, False, None]:
            raise ValueError(
                "unexpected argument {!r}, "
                "expected one of True, False, None".format(value))
        self._export_values = value

    def statements(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        var = registry.register(self.cursor, self)
        is_scoped = self.cursor.is_scoped_enum()

        yield "" # spacer

        yield "auto {var} = py::enum_<{enum}>({args});".format(
            var=var,
            enum=self.fully_qualified_name,
            args=join_arguments(
                parent,
                quote(self.expose_as),
                "py::arithmetic()" if self.arithmetic else None,
            ),
        )

        for child in cutils.children_by_kind(
                self.cursor, CursorKind.ENUM_CONSTANT_DECL):
            yield "{var}.value({name}, {field});".format(
                var=var,
                name=quote(child.spelling),
                field="{}::{}".format(
                    cutils.fully_qualified_name(
                        self.cursor if is_scoped else self.parent_cursor),
                    child.spelling,
                ),
            )

        export_values = self.export_values
        if export_values is None:
            export_values = not is_scoped

        if export_values:
            yield "{var}.export_values();".format(var=var)

        yield "" # spacer
