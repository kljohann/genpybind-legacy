#include "variables.h"

int SomeStruct::static_field = 1;
const int SomeStruct::static_const_field;
constexpr int SomeStruct::static_constexpr_field;
int SomeStruct::static_readonly_field = 4;
int SomeStruct::static_writable_false_field = 5;

int SomeClass::static_field = 1;
const int SomeClass::static_const_field;
constexpr int SomeClass::static_constexpr_field;
int SomeClass::static_readonly_field = 4;
int SomeClass::static_writable_false_field = 5;

int var = 1;
const int const_var = 2;
