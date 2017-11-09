#include "expose_as.h"

dummy::dummy(int value) : member(true), m_value(value) {}
bool dummy::function() { return true; }
int dummy::hash() const { return m_value; }
dummy::operator int() const { return m_value; }
constexpr bool dummy::constant;
void free_function() {}
X const x{15};
