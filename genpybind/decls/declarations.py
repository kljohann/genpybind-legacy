from __future__ import unicode_literals

from clang import cindex
from clang.cindex import AccessSpecifier

from .. import cutils, utils



class Visibility(object):  # pylint: disable=too-few-public-methods
    def __init__(self, value, allow_unspecified=False):
        self.value = value
        if any(value is v for v in (True, False, None)):
            return
        if allow_unspecified and value is ():  # pylint: disable=literal-comparison
            return
        raise ValueError("{!r} is not a valid visibility".format(value))

    def __eq__(self, other):
        if isinstance(other, Visibility):
            return self.value is other.value
        return self.value is other

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        raise TypeError("visibility used as bool")

    __bool__ = __nonzero__

    VISIBLE = None
    HIDDEN = None
    DEFAULT = None
    UNSPECIFIED = None

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
        self._cursor = cursor
        self._parent_cursor = cursor.semantic_parent
        self._default_visibility = default_visibility
        self._expose_as = None
        self._tags = set()
        self._visibility = Visibility.UNSPECIFIED

    def __str__(self):
        return "[{} {} {}]".format(
            self.__class__.__name__, self.cursor.kind, self.fully_qualified_name)

    def __repr__(self):
        return str(self)

    @property
    def fully_qualified_name(self):
        return cutils.fully_qualified_name(
            self.cursor, parent_cursor=self.parent_cursor)

    @property
    def spelling(self):
        return self.cursor.spelling

    @property
    def cursor(self):
        return self._cursor

    @property
    def parent_cursor(self):
        return self._parent_cursor

    def set_parent_cursor(self, parent_cursor):
        if not isinstance(parent_cursor, cindex.Cursor):
            raise TypeError("expected cursor type")
        self._parent_cursor = parent_cursor

    @property
    def expose_as(self):
        return self._expose_as or self.spelling

    def set_expose_as(self, name):
        self._expose_as = utils.convert_none(str, name)

    @property
    def tags(self):
        return frozenset(self._tags)

    def set_tag(self, *values):
        self._tags.update(values)

    def set_tags(self, *values):
        self._tags.update(values)

    @property
    def default_visibility(self):
        return self._default_visibility

    @property
    def visibility(self):
        return self._visibility

    @property
    def visible(self):
        if self.cursor.access_specifier in [
                AccessSpecifier.PROTECTED, AccessSpecifier.PRIVATE]:
            return False
        if not self.expose_as:
            return False
        if self.visibility in [Visibility.DEFAULT, Visibility.UNSPECIFIED]:
            return self.default_visibility
        return self.visibility == Visibility.VISIBLE

    def set_visible(self, value=True):
        self._visibility = Visibility(value)

    def set_hidden(self):
        self._visibility = Visibility.HIDDEN

    @property
    def implicit(self):
        return self.cursor.is_implicit()

    def expose(self, parent, registry):
        if not self.visible:
            return

        if not registry.should_expose(self):
            registry.register(self.cursor, None)
            return

        for result in self.statements(parent, registry):
            yield result

    def statements(self, _parent, _registry):
        yield "// FIXME: expose {}".format(self)
