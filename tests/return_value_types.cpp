#include "return_value_types.h"

bool return_builtin() { return {}; }
X return_class() { return {}; }

constexpr int example::Y::N;

example::Y example::return_class_in_namespace() { return {}; }
example::Y return_class_outside_namespace() { return {}; }

std::array<example::Y, example::Y::N> return_template_outside_namespace() {
  return {};
}

namespace example {
std::array<Y, Y::N> return_template_in_namespace();
} // namespace example
