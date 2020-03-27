import collections
import re

from clang import cindex

from . import cutils
from .decls.declarations import Declaration

if False:  # pylint: disable=using-constant-test
    from typing import (  # pylint: disable=unused-import
        Dict, FrozenSet, Iterable, Iterator, Optional, Text, Union)


RE_NON_IDENTIFIER = re.compile(r"[^a-zA-Z0-9_]+")


class Registry(collections.Mapping):
    def __init__(self, tags=None):
        # type: (Optional[Iterable[Text]]) -> None
        self._declarations = {}  # type: Dict[Text, Optional[Declaration]]
        self._tags = frozenset(tags or [])  # type: FrozenSet[Text]

    def should_expose(self, declaration):
        # type: (Declaration) -> bool
        # TODO: Reconsider handling of tags for exclusion of types.  Currently
        # it's not possible to stop at the topmost scope that has been excluded
        # as declarations within could still have additional tags.
        if not self._tags or not declaration.tags:
            return True
        return bool(self._tags.intersection(declaration.tags))

    def add_tombstone(self, cursor):
        # type: (cindex.Cursor) -> None
        """Add a tombstone that marks a type, which has been excluded via tags,
        as 'exposed elsewhere'.
        """
        # Types that have been excluded via tags are marked using `None`.
        # TODO: Use value different from None to encode this.
        self.register(cursor, None)

    @staticmethod
    def identifier(thing):
        # type: (Union[Declaration, cindex.Cursor]) -> Text
        if isinstance(thing, Declaration):
            thing = thing.cursor
        if not isinstance(thing, cindex.Cursor):
            raise TypeError("expected cursor, got {!r}".format(thing))

        prefix = "genpybind_{}_{{}}".format(thing.kind.name.lower())

        if thing.mangled_name:
            # Use the mangled name to disambiguate function overloads
            return prefix.format(thing.mangled_name)

        if thing.kind in cutils.TYPE_KINDS:
            fqn = thing.type.fully_qualified_name
        else:
            fqn = cutils.fully_qualified_name(thing)

        if not fqn:
            raise RuntimeError(
                "could not determine fully qualified name of {!r}".format(thing))

        parts = filter(None, [fqn, thing.displayname])
        return prefix.format(RE_NON_IDENTIFIER.sub("_", "_".join(parts)))

    def __getitem__(self, thing):
        # type: (Union[Declaration, cindex.Cursor]) -> Optional[Declaration]
        key = self.identifier(thing)
        return self._declarations[key]

    def __iter__(self):
        # type: () -> Iterator[Text]
        return iter(self._declarations)

    def __len__(self):
        # type: () -> int
        return len(self._declarations)

    def has(self, thing):
        # type: (Union[Declaration, cindex.Cursor]) -> bool
        return self.identifier(thing) in self._declarations

    def register(self, cursor, declaration):
        # type: (cindex.Cursor, Optional[Declaration]) -> Text
        assert isinstance(cursor, cindex.Cursor)
        assert isinstance(declaration, (Declaration, type(None)))
        key = self.identifier(cursor)
        existing = self._declarations.get(key, None)
        if existing is not None:
            raise RuntimeError("{} has conflicting entry in registry {!r}".format(
                cutils.fully_qualified_name(cursor), existing))
        self._declarations[key] = declaration
        return key
