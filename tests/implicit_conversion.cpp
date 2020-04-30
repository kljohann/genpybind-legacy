#include "implicit_conversion.h"

Value::Value(One /*one*/) : value(1) {}
Value::Value(Two /*two*/) : value(2) {}
Value::Value(Three /*three*/) : value(3) {}
Value::Value(float value) : value(value) {}
Value::Value(int value) : value(value) {}

int test_value(Value value) { return value.value; }
int test_by_reference(ByReference instance) { return instance.value; }
