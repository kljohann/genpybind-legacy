from ..utils import quote
from .level import Level

if False:  # pylint: disable=using-constant-test
    from ..registry import Registry  # pylint: disable=unused-import
    from .declarations import Declaration  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        Any, Iterable, Optional, Text, Tuple, Union)

class Namespace(Level):
    __slots__ = (
        "_module",
    )

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(Namespace, self).__init__(*args, **kwargs)
        self._module = None  # type: Optional[Text]

    @property
    def module(self):
        # type: () -> Optional[Text]
        return self._module

    def set_module(self, value=""):
        # type: (Optional[Text]) -> None
        self._module = str(value or "")

    def expose(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if self.visible is False:
            return

        # Only expose module if there is a matching tag.
        # TODO: Consider applying this check for all namespaces here, this
        # would amount to not descending to the nested declarations at all.
        if self.module is not None and not registry.should_expose(self):
            registry.add_tombstone(self.cursor)
            # TODO: In principle it would be necessary to visit all
            # declarations contained in this scope and add them to the
            # blacklist in turn.  This is however only used to prevent an
            # `opaque(false)` typedef from force-exposing a type that is
            # already exposed in a different module.
            return

        for result in self.statements(parent, registry):
            yield result

    def statements(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        scope = parent

        # Only expose module if there is a matching tag.
        # Else nested declarations will be put in the parent namespace.
        if self.module is not None and registry.should_expose(self):
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
