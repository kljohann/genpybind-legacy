from __future__ import unicode_literals

import collections
import re

from clang import cindex

from . import cutils
from .decls import Declaration


RE_NON_IDENTIFIER = re.compile(r"[^a-zA-Z0-9_]+")


class Registry(collections.Mapping):
    def __init__(self, tags=None):
        self._declarations = {}
        self._tags = set(tags or [])

    def should_expose(self, declaration):
        if not self._tags or not declaration.tags:
            return True
        return bool(self._tags.intersection(declaration.tags))

    @staticmethod
    def identifier(thing):
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

    def __getitem__(self, key):
        key = self.identifier(key)
        return self._declarations[key]

    def __iter__(self):
        return iter(self._declarations)

    def __len__(self):
        return len(self._declarations)

    def has(self, key):
        key = self.identifier(key)
        return key in self._declarations

    def register(self, cursor, declaration):
        assert isinstance(cursor, cindex.Cursor)
        assert isinstance(declaration, (Declaration, type(None)))
        key = self.identifier(cursor)
        existing = self._declarations.get(key, None)
        if existing is not None:
            raise RuntimeError("{} has conflicting entry in registry {!r}".format(
                cutils.fully_qualified_name(cursor), existing))
        self._declarations[key] = declaration
        return key
