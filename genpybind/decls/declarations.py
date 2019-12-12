from __future__ import unicode_literals

from clang import cindex
from clang.cindex import AccessSpecifier

from .. import cutils

if False:  # pylint: disable=using-constant-test
    from clang.cindex import Cursor  # pylint: disable=unused-import
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        Any, FrozenSet, Iterable, Optional, Set, Text, Tuple, Union)


class Visibility(object):  # pylint: disable=too-few-public-methods
    def __init__(self, value, allow_unspecified=False):
        # type: (Union[bool, None, Tuple[()]], bool) -> None
        self.value = value
        if any(value is v for v in (True, False, None)):
            return
        if allow_unspecified and value is ():  # pylint: disable=literal-comparison
            return
        raise ValueError("{!r} is not a valid visibility".format(value))

    def __eq__(self, other):
        # type: (Any) -> bool
        if isinstance(other, Visibility):
            return self.value is other.value
        return self.value is other

    def __ne__(self, other):
        # type: (Any) -> bool
        return not self == other

    def __nonzero__(self):
        # type: () -> bool
        raise TypeError("visibility used as bool")

    __bool__ = __nonzero__

    VISIBLE = None  # type: Visibility
    HIDDEN = None  # type: Visibility
    DEFAULT = None  # type: Visibility
    UNSPECIFIED = None  # type: Visibility

Visibility.VISIBLE = Visibility(True)
Visibility.HIDDEN = Visibility(False)
Visibility.DEFAULT = Visibility(None)
Visibility.UNSPECIFIED = Visibility((), allow_unspecified=True)


class Declaration(object):
    __slots__ = (
        "_cursor",
        "_parent_cursor",
        "_default_visibility",
        "_visibility",
        "_expose_as",
        "_tags",
    )

    def __init__(self, cursor, default_visibility=True, **_kwargs):
        # type: (Cursor, bool, **Any) -> None
        self._cursor = cursor
        self._parent_cursor = cursor.semantic_parent
        self._default_visibility = default_visibility  # type: bool
        self._visibility = Visibility.UNSPECIFIED
        self._expose_as = None  # type: Optional[Text]
        self._tags = set()  # type: Set[Text]

    def __str__(self):  # type: ignore
        # type: () -> Text
        return "[{} {} {}]".format(
            self.__class__.__name__, self.cursor.kind, self.fully_qualified_name)

    __repr__ = __str__  # type: ignore

    @property
    def fully_qualified_name(self):
        # type: () -> Text
        return cutils.fully_qualified_name(
            self.cursor, parent_cursor=self.parent_cursor)

    @property
    def spelling(self):
        # type: () -> Text
        return self.cursor.spelling

    @property
    def cursor(self):
        # type: () -> Cursor
        return self._cursor

    @property
    def parent_cursor(self):
        # type: () -> Cursor
        return self._parent_cursor

    def set_parent_cursor(self, parent_cursor):
        # type: (Cursor) -> None
        # check that argument is a cursor (else this may be used as an annotation by accident)
        if not isinstance(parent_cursor, cindex.Cursor):
            raise TypeError("expected cursor type")
        self._parent_cursor = parent_cursor

    @property
    def expose_as(self):
        # type: () -> Text
        return self._expose_as or self.spelling

    def set_expose_as(self, name):
        # type: (Optional[Text]) -> None
        if name is not None:
            name = str(name)
        self._expose_as = name

    @property
    def tags(self):
        # type: () -> FrozenSet[Text]
        return frozenset(self._tags)

    def set_tag(self, *values):
        # type: (*Text) -> None
        self._tags.update(values)

    def set_tags(self, *values):
        # type: (*Text) -> None
        self._tags.update(values)

    @property
    def default_visibility(self):
        # type: () -> bool
        return self._default_visibility

    @property
    def visibility(self):
        # type: () -> Visibility
        return self._visibility

    @property
    def visible(self):
        # type: () -> bool
        if self.cursor.access_specifier in [
                AccessSpecifier.PROTECTED, AccessSpecifier.PRIVATE]:
            return False
        if not self.expose_as:
            return False
        if self.visibility in [Visibility.DEFAULT, Visibility.UNSPECIFIED]:
            return self.default_visibility
        return self.visibility == Visibility.VISIBLE

    def set_visible(self, value=True):
        # type: (Optional[bool]) -> None
        self._visibility = Visibility(value)

    def set_hidden(self):
        # type: () -> None
        self._visibility = Visibility.HIDDEN

    @property
    def implicit(self):
        # type: () -> bool
        return self.cursor.is_implicit()

    def expose(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if not self.visible:
            return

        if not registry.should_expose(self):
            registry.register(self.cursor, None)
            return

        for result in self.statements(parent, registry):
            yield result

    def expose_later(self, _toplevel, _parent, _registry):
        # type: (Text, Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        raise RuntimeError("expose_later called on {}".format(self.__class__.__name__))

    def statements(self, _parent, _registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        yield "// FIXME: expose {}".format(self)
