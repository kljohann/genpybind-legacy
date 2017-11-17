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


class Klass(Level):
    __slots__ = (
        "_dynamic_attr",
        "_hide_base",
        "_inline_base",
    )

    def __init__(self, *args, **kwargs):
        super(Klass, self).__init__(*args, **kwargs)
        self._dynamic_attr = False
        self._hide_base = set()
        self._inline_base = set()

        if self.cursor.spelling != self.cursor.displayname:
            # most probably a template specialization
            self.set_expose_as(
                RE_NON_IDENTIFIER.sub("_", self.cursor.displayname))

    @property
    def fully_qualified_name(self):
        assert cutils.is_valid_type(self.cursor.type)
        return self.cursor.type.fully_qualified_name

    @property
    def dynamic_attr(self):
        return self._dynamic_attr

    def set_dynamic_attr(self, value=True):
        self._dynamic_attr = bool(value)

    @property
    def hide_base(self):
        return frozenset(self._hide_base)

    def set_hide_base(self, *patterns):
        self._hide_base.update(patterns)

    @property
    def inline_base(self):
        return frozenset(self._inline_base)

    def set_inline_base(self, *patterns):
        self._inline_base.update(patterns)

    def bases(self):
        """
        Returns mixed list of visible/non-hidden base classes which contains cursors for non-inlined
        base classes and Klass instances for inlined base classes.
        """
        bases = []
        hide_base = utils.compile_globs(self._hide_base)
        inline_base = utils.compile_globs(self._inline_base)
        for child in cutils.children_by_kind(
                self.cursor, CursorKind.CXX_BASE_SPECIFIER):
            if hide_base.match(child.displayname):
                continue
            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            if inline_base.match(child.displayname):
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
                declaration.set_inline_base(*self.inline_base)
                bases.append(declaration)
            else:
                bases.append(child)
        return bases

    def base_specifiers(self):
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
        declarations = []
        spellings = set()

        for child in [self] + self.bases():
            if child is self:
                # First process declarations of the class itself.
                child_declarations = self.children
            elif isinstance(child, Klass):
                # Process declarations of an inlined base class.
                child_declarations = child.declarations()
            else:
                # Non-inlined base classes do not directly contribute declarations.
                assert isinstance(child, cindex.Cursor)
                continue

            child_spellings = set()
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
        # may have already been registered as an opaque typedef
        if registry.has(self.cursor):
            var = registry.identifier(registry[self.cursor])
        else:
            var = registry.register(self.cursor, self)
        classes = [self.fully_qualified_name]
        classes.extend(self.base_specifiers())

        yield "" # spacer

        yield "auto {var} = py::class_<{classes}>({args});".format(
            var=var,
            classes=", ".join(classes),
            args=join_arguments(
                parent,
                quote(self.expose_as),
                "py::dynamic_attr()" if self.dynamic_attr else None,
            ),
        )

        yield "" # spacer

        properties = {}

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

            for declaration in declarations:
                typedef_name = registry.register(declaration.cursor, declaration)
                yield declaration.typedef(typedef_name)

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
