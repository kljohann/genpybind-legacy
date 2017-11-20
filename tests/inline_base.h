#pragma once

#include "genpybind.h"

struct Base {
  int member_function() const { return 42; }
};

// Needs PR 855 / pybind11 2.2.0 to work
struct GENPYBIND(visible, inline_base("*Base")) Derived : public Base {};

// TODO: Add example with multiple base classes
// TODO: Add more complex match expressions
