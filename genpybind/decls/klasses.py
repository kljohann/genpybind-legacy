from __future__ import unicode_literals

from clang import cindex
from clang.cindex import AccessSpecifier, CursorKind

from .. import cutils, utils
from ..registry import RE_NON_IDENTIFIER
from ..utils import join_arguments, quote
from .constructors import Constructor
from .gather import gather_declarations
from .level import Level
from .methods import Method

if False:  # pylint: disable=using-constant-test
    from ..registry import Registry  # pylint: disable=unused-import
    from .declarations import Declaration  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        Any, Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Text, Tuple, Union)


class Klass(Level):
    __slots__ = (
        "_dynamic_attr",
        "_hide_base",
        "_inline_base",
        "_holder_type",
    )

    filter_bases = ['*std::enable_shared_from_this*']

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(Klass, self).__init__(*args, **kwargs)
        self._dynamic_attr = False
        self._hide_base = set(Klass.filter_bases)  # type: Set[Text]
        self._inline_base = set()  # type: Set[Text]
        self._holder_type = None  # type: Optional[Text]

        if self.cursor.spelling != self.cursor.displayname:
            # most probably a template specialization
            self.set_expose_as(
                RE_NON_IDENTIFIER.sub("_", self.cursor.displayname))

    @property
    def fully_qualified_name(self):
        # type: () -> Text
        assert cutils.is_valid_type(self.cursor.type)
        return self.cursor.type.fully_qualified_name

    @property
    def dynamic_attr(self):
        # type: () -> bool
        return self._dynamic_attr

    def set_dynamic_attr(self, value=True):
        # type: (bool) -> None
        self._dynamic_attr = bool(value)

    @property
    def hide_base(self):
        # type: () -> FrozenSet[Text]
        return frozenset(self._hide_base)

    def set_hide_base(self, *patterns):
        # type: (*Text) -> None
        self._hide_base.update(patterns)

    @property
    def inline_base(self):
        # type: () -> FrozenSet[Text]
        return frozenset(self._inline_base)

    def set_inline_base(self, *patterns):
        # type: (*Text) -> None
        self._inline_base.update(patterns)

    @property
    def holder_type(self):
        # type: () -> Optional[Text]
        return self._holder_type

    def set_holder_type(self, holder_type):
        # type: (Optional[Text]) -> None
        self._holder_type = holder_type

    def bases(self):
        # type: () -> List[Union[cindex.Cursor, Klass]]
        """
        Returns mixed list of visible/non-hidden base classes which contains cursors for non-inlined
        base classes and Klass instances for inlined base classes.
        """
        bases = []  # type: List[Union[cindex.Cursor, Klass]]
        hide_base = utils.compile_globs(self._hide_base)
        inline_base = utils.compile_globs(self._inline_base)
        for child in cutils.children_by_kind(
                self.cursor, CursorKind.CXX_BASE_SPECIFIER):
            name = child.type.fully_qualified_name
            if hide_base.match(name):
                continue
            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            if inline_base.match(name):
                if child.referenced.kind == CursorKind.NO_DECL_FOUND:
                    # FIXME: Warning?
                    # assert False, child.type.fully_qualified_name
                    continue
                if child.referenced.kind not in cutils.RECORD_KINDS:
                    assert False, child.referenced.kind
                    continue
                declarations = gather_declarations(
                    child.referenced, default_visibility=True)
                if not declarations:
                    raise RuntimeError(
                        "could not load declaration when inlining {}".format(self))
                declaration = declarations[0]
                assert isinstance(declaration, Klass)
                declaration.set_inline_base(*self.inline_base)
                bases.append(declaration)
            else:
                bases.append(child)
        return bases

    def base_specifiers(self):
        # type: () -> List[Text]
        bases = []

        for child in self.bases():
            if isinstance(child, cindex.Cursor):
                # TODO: This produces "boost::operators_impl::equality_comparable" for
                # e.g. "boost::equality_comparable<marocco::LogicalNeuron>".
                bases.append(child.type.fully_qualified_name)
                continue
            bases.extend(child.base_specifiers())

        return bases

    def declarations(self):
        # type: () -> List[Declaration]
        declarations = []
        spellings = set()  # type: Set[Text]

        child = None  # type: Union[None, cindex.Cursor, Klass]
        for child in [self] + self.bases():  # type: ignore
            assert child is not None
            if child is self:
                # First process declarations of the class itself.
                child_declarations = self.children  # type: Sequence[Declaration]
            elif isinstance(child, Klass):
                # Process declarations of an inlined base class.
                child_declarations = child.declarations()
            else:
                # Non-inlined base classes do not directly contribute declarations.
                assert isinstance(child, cindex.Cursor)
                continue

            child_spellings = set()  # type: Set[Text]
            for decl in child_declarations:
                # If the declaration is hidden or a declaration/overload with the same name
                # has already been defined by an earlier class, skip this declaration (shadowing).
                if not decl.visible or decl.spelling in spellings:
                    continue
                # Only process constructors of the original class itself.
                if isinstance(decl, Constructor) and child is not self:
                    continue
                decl.set_parent_cursor(self.cursor)
                declarations.append(decl)
                child_spellings.add(decl.spelling)
            spellings.update(child_spellings)

        return declarations

    def expose(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if not self.visible:
            return

        if not registry.should_expose(self):
            registry.register(self.cursor, None)
            # We need to give child declarations the chance to
            # blacklist cursors in the registry.
            for declaration in self.declarations():
                # As each child declaration has the same tags
                # it is not allowed to be exposed, too.
                declaration.expose(parent, registry)
            return

        for result in self.statements(parent, registry):
            yield result

    def statements(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        # may have already been registered as an opaque typedef
        if registry.has(self.cursor):
            decl = registry[self.cursor]
            assert decl is not None
            var = registry.identifier(decl)
        else:
            var = registry.register(self.cursor, self)
        options = [self.fully_qualified_name] + self.base_specifiers()
        if self.holder_type is not None:
            options.append(self.holder_type)

        yield "" # spacer

        yield "auto {var} = py::class_<{classes}>({args});".format(
            var=var,
            classes=", ".join(options),
            args=join_arguments(
                parent,
                quote(self.expose_as),
                "py::dynamic_attr()" if self.dynamic_attr else None,
            ),
        )

        yield "" # spacer

        properties = {}  # type: Dict[Text, Dict[Text, Method]]

        for declaration in self.declarations():
            if isinstance(declaration, Method) and declaration.accessor_for:
                for name, access_type in declaration.accessor_for.items():
                    accessors = properties.setdefault(name, {})
                    if access_type in accessors:
                        existing = accessors[access_type]
                        raise RuntimeError(
                            "conflicting {!r} accessors for property {!r}: {} and {}".format(
                                access_type, name, existing, declaration))
                    accessors[access_type] = declaration
                continue

            for result in declaration.expose(var, registry):
                yield result

        # TODO: check registry.should_expose(...)
        for name, accessors in properties.items():
            if "get" not in accessors:
                raise RuntimeError(
                    "missing getter for property {} of {}".format(name, self))

            writable = "set" in accessors
            declarations = [accessors["get"]]
            if writable:
                declarations.append(accessors["set"])

            # TODO: support overloaded methods for setters/getters

            qualifier = "" if writable else "_readonly"
            yield "{var}.def_property{qualifier}({args});".format(
                var=var,
                qualifier=qualifier,
                args=join_arguments(
                    quote(name),
                    [decl.function_object() for decl in declarations]
                ),
            )

        yield "" # spacer
