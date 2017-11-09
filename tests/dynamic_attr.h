#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Default {
  void some_function() const {}
  bool existing_field = true;
};

struct GENPYBIND(dynamic_attr) WithDynamic {
  void some_function() const {}
  bool existing_field = true;
};
