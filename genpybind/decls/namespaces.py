from ..utils import quote
from .level import Level

class Namespace(Level):
    __slots__ = (
        "_module",
    )

    def __init__(self, *args, **kwargs):
        super(Namespace, self).__init__(*args, **kwargs)
        self._module = None

    @property
    def module(self):
        return self._module

    def set_module(self, value=""):
        self._module = value

    def expose(self, parent, registry):
        if self.visible is False:
            return

        for result in self.statements(parent, registry):
            yield result

    def statements(self, parent, registry):
        scope = parent
        if self.module is not None:
            yield "" # spacer
            # Namespaces may be redeclared.
            if registry.has(self.cursor.canonical):
                # We do not need to register the module again.
                scope = registry.identifier(self.cursor.canonical)
            else:
                scope = registry.register(self.cursor.canonical, self)
                yield "py::module {var} = {parent}.def_submodule({name}, {doc});".format(
                    var=scope,
                    parent=parent,
                    name=quote(self.module or self.expose_as),
                    doc=quote(self.cursor.brief_comment),
                )

        for declaration in self.children:
            for result in declaration.expose(scope, registry):
                yield result

        if self.module is not None:
            yield "" # spacer
