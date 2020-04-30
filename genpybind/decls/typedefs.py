from __future__ import unicode_literals

from .. import cutils
from ..utils import quote
from .declarations import Declaration
from .gather import gather_declarations

if False:  # pylint: disable=using-constant-test
    from clang import cindex  # pylint: disable=unused-import
    from ..annotations import Annotations  # pylint: disable=unused-import
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        Any, Iterable, Optional, Text, Tuple, Union)


class Typedef(Declaration):
    __slots__ = (
        "_annotations",
        "_opaque",
    )

    def __init__(self, cursor, annotations=None, **kwargs):
        # type: (cindex.Cursor, Optional[Annotations], **Any) -> None
        super(Typedef, self).__init__(cursor, annotations=annotations, **kwargs)
        assert annotations is not None
        self._annotations = annotations
        # expose as alias
        self._opaque = None  # type: Optional[bool]

    @property
    def default_visibility(self):
        # type: () -> bool
        # Typedefs have to be made visible explicitly.
        return False

    @property
    def opaque(self):
        # type: () -> Optional[bool]
        return self._opaque

    def set_opaque(self, value=True):
        # type: (Optional[bool]) -> None
        self._opaque = bool(value)

    def set(self, _name, *_args):  # pylint: disable=no-self-use
        # type: (Text, *Any) -> bool
        # We already capture annotations in the ctor.
        return True

    def underlying_cursor(self):
        # type: () -> cindex.Cursor
        return cutils.typedef_underlying_declaration(self.cursor)

    def expose_later(self, toplevel, parent, registry):
        # type: (Text, Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        assert not self.opaque

        decl_cursor = self.underlying_cursor()

        # If this typedef is marked `opaque(false)` and the type has neither
        # already been exposed nor marked as "exposed elsewhere", try to expose
        # it now:
        if self.opaque is False and not registry.has(decl_cursor):
            declarations = gather_declarations(decl_cursor, default_visibility=True)
            if not declarations:
                raise RuntimeError(
                    "could not load declaration when exposing {}".format(self))
            declaration = declarations[0]

            self._annotations.apply_to(declaration, exclude=["opaque"])
            for result in declaration.expose(toplevel, registry):
                yield result

            # retrigger expose_later to expose the alias
            yield (self, parent)
            return

        # If the target type is visible and not blacklisted via mismatched tags
        # (see Registry.should_expose) it should have already been exposed at
        # this point.  For types exposed elsewhere we assume the corresponding
        # module to be present at run time.  As a consequence it's sensible to
        # unconditionally create an alias here.
        tpl = "genpybind_get_type_object<{}>()"
        obj = tpl.format(decl_cursor.type.fully_qualified_name)
        yield "{parent}.attr({name}) = {obj};".format(
            parent=parent,
            name=quote(self.expose_as),
            obj=obj,
        )

    def expose(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if not self.visible:
            return

        if not registry.should_expose(self):
            registry.add_tombstone(self.cursor)
            if self.opaque:
                decl_cursor = cutils.typedef_underlying_declaration(self.cursor)
                registry.add_tombstone(decl_cursor)
            return

        for result in self.statements(parent, registry):
            yield result

    def statements(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if not self.opaque:
            yield (self, parent)
            return

        decl_cursor = cutils.typedef_underlying_declaration(self.cursor)
        declarations = gather_declarations(decl_cursor, default_visibility=True)
        if not declarations:
            raise RuntimeError(
                "could not load declaration when exposing {}".format(self))
        declaration = declarations[0]
        declaration.set_expose_as(self.expose_as)

        registry.register(decl_cursor, self)
        self._annotations.apply_to(declaration, exclude=["opaque"])
        for result in declaration.expose(parent, registry):
            yield result
