#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) One {};
struct GENPYBIND(visible) Two {};
struct GENPYBIND(visible) Three {};

// Implicit conversions have to be annotated explicitly (the absence of the `explicit`
// keyword is not enough).

struct GENPYBIND(visible) Value {
  Value(One one);
  explicit Value(Two two);
  Value(Three three) GENPYBIND(implicit_conversion);
  Value(float value);
  Value(int value) GENPYBIND(implicit_conversion);

  int value;
};

GENPYBIND(visible)
int test_value(Value value);

// Implicit conversion should also work for reference types.

struct GENPYBIND(visible) Number {
  Number(int value) : value(value) {}
  int value;
};

struct GENPYBIND(visible) ByReference {
  /*implicit*/ ByReference(Number const &number) GENPYBIND(implicit_conversion)
      : value(number.value) {}
  int value;
};

GENPYBIND(visible)
int test_by_reference(ByReference instance);
