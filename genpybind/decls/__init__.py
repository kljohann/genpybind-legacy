from __future__ import unicode_literals

from clang.cindex import CursorKind

from .declarations import Declaration
from .constructors import Constructor
from .enums import Enum
from .callables import Function
from .klasses import Klass
from .manual import Manual
from .methods import Method
from .namespaces import Namespace
from .operators import Operator
from .typedefs import Typedef
from .variables import FieldOrVar

from .gather import DECLARATION_TYPES, gather_declarations

# FIXME: clean up
DECLARATION_TYPES.update({
    CursorKind.CLASS_DECL: Klass,
    CursorKind.CONSTRUCTOR: Constructor,
    CursorKind.CONVERSION_FUNCTION: Operator.or_else(Method),
    CursorKind.CXX_METHOD: Operator.or_else(Method),
    CursorKind.FRIEND_DECL: Operator.or_else(None),
    CursorKind.ENUM_DECL: Enum,
    CursorKind.FIELD_DECL: FieldOrVar,
    CursorKind.FUNCTION_DECL: Function,
    CursorKind.NAMESPACE: Namespace,
    CursorKind.STRUCT_DECL: Klass,
    CursorKind.TYPEDEF_DECL: Typedef,
    CursorKind.VAR_DECL: FieldOrVar,
})
