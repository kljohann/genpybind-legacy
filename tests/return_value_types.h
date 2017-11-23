#pragma once

#include <array>

#include "genpybind.h"

struct GENPYBIND(visible) X {};

bool GENPYBIND(visible) return_builtin();
X GENPYBIND(visible) return_class();

namespace example {
struct GENPYBIND(visible) Y {
  static constexpr int N = 1;
};

Y GENPYBIND(visible) return_class_in_namespace();
} // namespace example

example::Y GENPYBIND(visible) return_class_outside_namespace();

std::array<example::Y, example::Y::N> GENPYBIND(visible) return_template_outside_namespace();

// TODO: genpybind fails to expand `Y::N` to fully qualified expression
/*
namespace example {
std::array<Y, Y::N> GENPYBIND(visible) return_template_in_namespace();
} // namespace example
*/
