from clang.cindex import AvailabilityKind, CursorKind

from .. import cutils
from ..annotations import Annotations
from ..cutils import RECORD_KINDS, SCOPE_CURSOR_KINDS
from .declarations import Visibility
from .level import Level
from .manual import Manual
from .namespaces import Namespace

if False:  # pylint: disable=using-constant-test
    from .declarations import Declaration  # pylint: disable=unused-import
    from clang.cindex import Cursor  # pylint: disable=unused-import
    from typing import Dict, Iterable, List, Optional, Tuple, Type, Union  # pylint: disable=unused-import

# will be populated in genpybind/decls/__init__.py
DECLARATION_TYPES = {}  # type: Dict[CursorKind, Type[Declaration]]
UNAVAILABLE_KINDS = frozenset([AvailabilityKind.NOT_AVAILABLE, AvailabilityKind.NOT_ACCESSIBLE])

def gather_declarations(cursor, default_visibility=False):
    # type: (Cursor, bool) -> List[Declaration]
    toplevel_declarations = []  # type: List[Declaration]
    queue = [([], cursor, default_visibility)]  # type: List[Tuple[List[Level], Cursor, bool]]
    while queue:
        parent_declarations, cursor, default_visibility = queue.pop(0)

        if cursor.availability in UNAVAILABLE_KINDS:
            # Declaration may be unavailable (e.g. deleted constructor).
            continue

        annotations = Annotations.from_cursor(cursor)
        declaration = None  # type: Optional[Declaration]

        # Check for GENPYBIND_MANUAL instructions
        if cursor.kind == CursorKind.VAR_DECL and any(k == "manual" for k, _ in annotations):
            child = cutils.first_by_kind_bfs(cursor, CursorKind.LAMBDA_EXPR)
            if child is not None:
                child = cutils.first_by_kind_bfs(child, CursorKind.COMPOUND_STMT)
                declaration = Manual(cursor, code=child)

        # As we do not descend into friend declarations we have to explicitly
        # lift the annotations of its children, s.t. they apply directly.
        # For example, one might expect to be able to write:
        #     friend std::ostream& operator<<(
        #         std::ostream& os, const X& x) GENPYBIND(stringstream);
        # As all annotations are also applied to the referenced declaration,
        # they have to be accepted and ignored there.  In this case, Function
        # needs to support set_stringstream, for example.
        if cursor.kind == CursorKind.FRIEND_DECL:
            for child in cursor.get_children(
                    with_implicit=True, with_template_instantiations=True):
                # TODO: Since "visible", "hidden" etc. also get passed through,
                #       this is only enabled for friend declarations of operators
                #       to limit the impact/scope of this change.
                if not child.spelling.startswith("operator"):
                    continue
                child_annotations = Annotations.from_cursor(child)
                annotations.extend(child_annotations)

        # For function templates we explicitly request all template instantiations
        # and add them to the queue.
        if cursor.kind == CursorKind.FUNCTION_TEMPLATE:
            for child in cursor.get_children(
                    with_implicit=True, with_template_instantiations=True):
                if child.kind in [
                        CursorKind.CONSTRUCTOR,
                        CursorKind.CONVERSION_FUNCTION,
                        CursorKind.CXX_METHOD,
                        CursorKind.FUNCTION_DECL,
                ]:
                    queue.append((parent_declarations, child, default_visibility))
            continue

        if cursor.kind == CursorKind.CLASS_TEMPLATE:
            # FIXME: Support explicit instantiation of template classes
            continue

        if declaration is None and cursor.kind in DECLARATION_TYPES:
            declaration = DECLARATION_TYPES[cursor.kind](
                cursor, default_visibility=default_visibility,
                annotations=annotations)

        if cursor.kind in RECORD_KINDS:
            if not cursor.is_definition():
                # We do not want to expose forward declarations.
                continue
            if cursor.is_implicit():
                # Records have an implicit nested forward declaration of their
                # existence, which we do not want to represent/wrap.
                if cursor.semantic_parent is None:
                    pass
                elif cutils.is_same_type(cursor.type, cursor.semantic_parent.type):
                    declaration = None


        if declaration is not None:
            try:
                annotations.apply_to(declaration)
            except:
                print("// {}".format(declaration))
                print("// at {}:{}:{}".format(
                    cursor.location.file.name,
                    cursor.location.line,
                    cursor.location.column))
                raise

            has_explicit_visibility = declaration.visibility != Visibility.UNSPECIFIED

            if not isinstance(declaration, Namespace):
                if annotations and not has_explicit_visibility:
                    # If visibility has not been specified explicitly but there
                    # were any annotations we default to visible.
                    # (except for namespaces).
                    declaration.set_visible(True)

                # Visibility is inherited by child scopes
                default_visibility = declaration.visible
            elif not has_explicit_visibility:
                # Namespaces default to visible (but visibility is not inherited)
                declaration.set_visible(True)
            else:
                # Explicitly specified visibility is inherited by child scopes
                default_visibility = declaration.visible

            # Do not descend into hidden declarations
            if not declaration.visible:
                continue

            for parent in parent_declarations:
                declaration.set_tags(*parent.tags)

            if parent_declarations:
                parent_declarations[0].add_child(declaration)
            else:
                toplevel_declarations.append(declaration)

        if cursor.kind not in SCOPE_CURSOR_KINDS:
            continue

        if declaration is not None:
            assert isinstance(declaration, Level)
            parent_declarations = [declaration] + parent_declarations[:]

        for child in cursor.get_children(
                with_implicit=True, with_template_instantiations=True):
            queue.append((parent_declarations, child, default_visibility))

    return toplevel_declarations
