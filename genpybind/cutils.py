from __future__ import unicode_literals

from clang.cindex import Cursor, CursorKind, TypeKind, TokenGroup, TokenKind

from . import utils


EXPRESSION_KINDS = frozenset({
    kind for kind in CursorKind.get_all_kinds()
    if kind.is_expression() and not kind.is_statement()
})


RECORD_KINDS = frozenset([
    CursorKind.CLASS_DECL,
    CursorKind.STRUCT_DECL,
])


TYPE_KINDS = frozenset([
    CursorKind.CLASS_DECL,
    CursorKind.STRUCT_DECL,
    CursorKind.TYPEDEF_DECL,
])


SCOPE_CURSOR_KINDS = frozenset([
    CursorKind.TRANSLATION_UNIT,
    CursorKind.NAMESPACE,
    CursorKind.CLASS_DECL,
    CursorKind.STRUCT_DECL,
])


def is_valid_type(type_):
    return type_.kind != TypeKind.INVALID


def is_same_type(lhs, rhs):
    # TODO: Retrieve non-const-qualified type instead
    def qualify(type_):
        name = type_.fully_qualified_name
        name = utils.strip_prefix(name, "const ")
        return name
    return qualify(lhs) == qualify(rhs)


def get_tokens_with_whitespace(cursor):
    return cursor.get_tokens(TokenGroup.TOKENIZE_KEEP_WHITESPACE)


def typedef_underlying_declaration(cursor):
    while cursor.kind == CursorKind.TYPEDEF_DECL:
        underlying_type = cursor.underlying_typedef_type
        cursor_ = underlying_type.get_declaration()
        if cursor_.kind == CursorKind.NO_DECL_FOUND:
            cursor_ = underlying_type.get_canonical().get_declaration()
        if cursor_.kind == CursorKind.NO_DECL_FOUND:
            break
        cursor = cursor_
    return cursor


def fully_qualified_name(thing, parent_cursor=None):
    if thing.kind == CursorKind.TRANSLATION_UNIT:
        # Happens e.g. for unscoped enums, which pass their parent_cursor
        return ""

    cursor = getattr(thing, "cursor", thing) # thing may be a token
    if thing is not cursor and cursor.referenced is not None:
        # cursor associated with token may be a type ref
        assert cursor.kind in [
            CursorKind.TYPE_REF,
            CursorKind.DECL_REF_EXPR,
            CursorKind.NAMESPACE_REF,
        ]
        # We should get the scope from the referenced cursor,
        # not from the token's location.
        cursor = cursor.referenced

    if cursor.kind in TYPE_KINDS:
        assert isinstance(cursor, Cursor)
        return cursor.type.fully_qualified_name

    parts = [thing.spelling]
    parent_cursor = parent_cursor or cursor.semantic_parent
    while parent_cursor is not None:
        if parent_cursor.kind == CursorKind.TRANSLATION_UNIT:
            break
        if parent_cursor.kind in TYPE_KINDS:
            parts.append(parent_cursor.type.fully_qualified_name)
            break
        parts.append(parent_cursor.spelling)
        parent_cursor = parent_cursor.semantic_parent
    return "::".join(reversed(filter(None, parts)))


def fully_qualified_expression(cursor):
    output = []
    current = [""]
    for token in get_tokens_with_whitespace(cursor):
        # FIXME: Handle leading token.spelling == "::"
        if token.kind == TokenKind.IDENTIFIER:
            if isinstance(current[0], basestring):
                output.append(current)
                current = [token]
            else:
                current.append(token.spelling)
        else:
            current.append(token.spelling)
    output.append(current)

    for tokens in output:
        assert len(tokens) > 0
        if not isinstance(tokens[0], basestring):
            tokens[0] = fully_qualified_name(tokens[0])

    return "".join(utils.flatten(output))


def first_by_kind_bfs(cursor, kinds):
    if not isinstance(kinds, (frozenset, set, list, tuple)):
        kinds = [kinds]

    queue = [cursor]
    while queue:
        cursor = queue.pop(0)

        if cursor.kind in kinds:
            return cursor

        for child in cursor.get_children(
                with_implicit=True, with_template_instantiations=True):
            queue.append(child)

    return None


def first_parent_by_kind(cursor, kinds):
    if not isinstance(kinds, (frozenset, set, list, tuple)):
        kinds = [kinds]

    while cursor:
        if cursor.kind in kinds:
            return cursor
        cursor = cursor.semantic_parent
    return None


def children_by_kind(cursor, kinds):
    if not isinstance(kinds, (frozenset, set, list, tuple)):
        kinds = [kinds]

    for child in cursor.get_children(
            with_implicit=True, with_template_instantiations=True):
        if child.kind in kinds:
            yield child
