#include "reference_member.h"

ReferenceMember::ReferenceMember(Nested& n) : nested(n) {}
Nested& ReferenceMember::get_nested() { return nested; }
void ReferenceMember::set_nested(Nested& n) { nested = n; }
