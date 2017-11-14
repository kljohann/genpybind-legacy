from __future__ import unicode_literals

from clang.cindex import CursorKind

from ..utils import quote
from .. import cutils
from .declarations import Declaration
from .enums import Enum
from .gather import gather_declarations
from .klasses import Klass


class Typedef(Declaration):
    __slots__ = (
        "_annotations",
        "_opaque",
    )

    def __init__(self, *args, **kwargs):
        super(Typedef, self).__init__(*args, **kwargs)
        self._annotations = kwargs["annotations"]
        self._opaque = None # expose as alias

    @property
    def default_visibility(self):
        # Typedefs have to be made visible explicitly.
        return False

    @property
    def opaque(self):
        return self._opaque

    def set_opaque(self, value=True):
        self._opaque = bool(value)

    def set(self, name, *args):
        # We already capture annotations in the ctor.
        return True

    def underlying_cursor(self):
        return cutils.typedef_underlying_declaration(self.cursor)

    def expose_later(self, toplevel, parent, registry):
        assert not self.opaque

        decl_cursor = cutils.typedef_underlying_declaration(self.cursor)
        decl = registry.get(decl_cursor, None)

        if self.exposed_elsewhere(registry) or decl is not None:
            tpl = "pybind_get_type_object<{}>()"
            obj = tpl.format(decl_cursor.type.fully_qualified_name)
            yield "{parent}.attr({name}) = {obj};".format(
                parent=parent,
                name=quote(self.expose_as),
                obj=obj,
            )
            return

        if self.opaque is None: # alias
            yield "// FIXME: expose {}".format(self)
            return

        assert self.opaque is False

        decl_cursor = self.underlying_cursor()
        declaration, = gather_declarations(decl_cursor, default_visibility=True)

        self._annotations.apply_to(declaration, exclude=["opaque"])
        for result in declaration.expose(toplevel, registry):
            yield result

        # retrigger expose_later to expose the alias
        yield (self, parent)

    def exposed_elsewhere(self, registry):
        decl_cursor = cutils.typedef_underlying_declaration(self.cursor)
        return registry.get(decl_cursor, True) is None

    def expose(self, parent, registry):
        if not self.visible:
            return

        if not registry.should_expose(self):
            registry.register(self.cursor, None)
            if self.opaque:
                decl_cursor = cutils.typedef_underlying_declaration(self.cursor)
                registry.register(decl_cursor, None)
            return

        for result in self.statements(parent, registry):
            yield result

    def statements(self, parent, registry):
        if not self.opaque:
            yield (self, parent)
            return

        decl_cursor = cutils.typedef_underlying_declaration(self.cursor)
        declaration, = gather_declarations(decl_cursor, default_visibility=True)
        declaration.set_expose_as(self.expose_as)

        registry.register(decl_cursor, self)
        self._annotations.apply_to(declaration, exclude=["opaque"])
        for result in declaration.expose(parent, registry):
            yield result
