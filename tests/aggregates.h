#pragma once

#include "genpybind.h"

// TODO: Aggregate constructor should be wrapped for pybind11 >= 2.2.0
struct GENPYBIND(visible) Aggregate {
  int a;
  int b;
  int c;
};
