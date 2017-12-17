# -*- mode: python; -*-
import typing
# TODO: Check that each use of typing.Text in this file is correct

class File(object):
    name: typing.Text

class SourceLocation(object):
    column: int
    file: File
    line: int

class TokenKind(object):
    IDENTIFIER: TokenKind

class Token(object):
    kind: TokenKind
    spelling: typing.Text

class TokenGroup(object):
    TOKENIZE_KEEP_WHITESPACE: int

class TypeKind(object):
    INVALID: TypeKind

class Type(object):
    fully_qualified_name: typing.Text
    kind: TypeKind
    spelling: typing.Text
    def argument_types(self) -> typing.Iterator[Type]: ...
    def get_canonical(self) -> Type: ...
    def get_declaration(self) -> Cursor: ...
    def get_pointee(self) -> Type: ...
    def get_result(self) -> Type: ...
    def is_const_qualified(self) -> bool: ...

class AvailabilityKind(object):
    NOT_ACCESSIBLE: AvailabilityKind
    NOT_AVAILABLE: AvailabilityKind

class AccessSpecifier(object):
    PRIVATE: AccessSpecifier
    PROTECTED: AccessSpecifier
    PUBLIC: AccessSpecifier

class CursorKind(object):
    name: typing.Text
    @staticmethod
    def get_all_kinds() -> typing.List[CursorKind]: ...
    def is_expression(self) -> bool: ...
    def is_statement(self) -> bool: ...

    ANNOTATE_ATTR: CursorKind
    CLASS_DECL: CursorKind
    CLASS_TEMPLATE: CursorKind
    COMPOUND_STMT: CursorKind
    CONSTRUCTOR: CursorKind
    CONVERSION_FUNCTION: CursorKind
    CXX_BASE_SPECIFIER: CursorKind
    CXX_METHOD: CursorKind
    DECL_REF_EXPR: CursorKind
    ENUM_CONSTANT_DECL: CursorKind
    ENUM_DECL: CursorKind
    FIELD_DECL: CursorKind
    FRIEND_DECL: CursorKind
    FUNCTION_DECL: CursorKind
    FUNCTION_TEMPLATE: CursorKind
    LAMBDA_EXPR: CursorKind
    NAMESPACE: CursorKind
    NAMESPACE_REF: CursorKind
    NO_DECL_FOUND: CursorKind
    PARM_DECL: CursorKind
    STRUCT_DECL: CursorKind
    TRANSLATION_UNIT: CursorKind
    TYPEDEF_DECL: CursorKind
    TYPE_REF: CursorKind
    VAR_DECL: CursorKind

class Cursor(object):
    access_specifier: AccessSpecifier
    availability: AvailabilityKind
    brief_comment: typing.Text
    canonical: Cursor
    displayname: typing.Text
    kind: CursorKind
    location: SourceLocation
    mangled_name: typing.Text
    referenced: Cursor
    semantic_parent: Cursor
    spelling: typing.Text
    type: Type
    underlying_typedef_type: Type
    def get_arguments(self) -> typing.Iterator[Cursor]: ...
    def get_children(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Iterator[Cursor]: ...
    def get_tokens(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Iterator[Token]:...
    def is_abstract_record(self) -> bool: ...
    def is_const_method(self) -> bool: ...
    def is_definition(self) -> bool: ...
    def is_implicit(self) -> bool: ...
    def is_move_constructor(self) -> bool: ...
    def is_scoped_enum(self) -> bool: ...
    def is_static_method(self) -> bool: ...

class Index(object):
    pass

class Diagnostic(object):
    children: typing.Iterator[Diagnostic]
    def format(self, options: typing.Optional[int]=None) -> typing.Text: ...

class TranslationUnit(object):
    cursor: Cursor
    diagnostics: typing.Iterator[Diagnostic]
    @classmethod
    def from_ast_file(cls, filename: typing.Text, index: typing.Optional[Index]=None) -> TranslationUnit: ...
