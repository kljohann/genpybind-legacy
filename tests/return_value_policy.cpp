#include "return_value_policy.h"

int Something::value() const { return m_nested.value; }
Nested &Something::ref() { return m_nested; }
const Nested &Something::cref() const { return m_nested; }
Nested &Something::ref_as_copy() { return m_nested; }
Nested &Something::ref_as_ref_int() { return m_nested; }
const Nested &Something::cref_as_ref_int() const { return m_nested; }
