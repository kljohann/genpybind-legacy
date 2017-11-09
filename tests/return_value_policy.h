#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Nested {
  int value = 0;
};

class GENPYBIND(visible) Something {
public:
  int value() const;

  Nested &ref();
  const Nested &cref() const;

  GENPYBIND(return_value_policy(copy))
  Nested &ref_as_copy();

  GENPYBIND(return_value_policy(reference_internal))
  Nested &ref_as_ref_int();

  GENPYBIND(return_value_policy(reference_internal))
  const Nested &cref_as_ref_int() const;

private:
  Nested m_nested;
};
