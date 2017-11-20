#include "operators.h"

int has_call::operator()(int value) const { return value; }
int has_call::operator()(int first, int second) const { return first + second; }

int has_floordiv::operator/(int div) const { return 42 / div; }
