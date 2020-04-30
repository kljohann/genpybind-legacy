#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Nested {
  Nested(int value = 0) : value(value) {}

  int value;
};

class GENPYBIND(visible) ReferenceMember {
public:
  ReferenceMember(Nested &n);

  // C++ can use the reference member directly
  GENPYBIND(hidden)
  Nested &nested;

  // Only needed for Python
  GENPYBIND(getter_for(nested), return_value_policy(reference_internal))
  Nested &get_nested();

  // Only needed for Python
  GENPYBIND(setter_for(nested))
  void set_nested(Nested &n);
};
