#pragma once

#include "genpybind.h"

struct DefinedLaterTarget;
struct GENPYBIND(visible) Target {};
struct UnexposedTarget {};

namespace visibility {

// Typedefs have to be made visible explicitly.
typedef Target typedef_not_visible;
typedef Target typedef_explicitly_visible GENPYBIND(visible);
typedef Target typedef_explicitly_hidden GENPYBIND(hidden);
typedef Target typedef_implicitly_visible GENPYBIND(opaque(false));

typedef UnexposedTarget typedef_unexposed_target GENPYBIND(visible);
typedef DefinedLaterTarget typedef_defined_later_target GENPYBIND(visible);

struct GENPYBIND(visible) VisibleParent {
  typedef Target typedef_not_visible;
  typedef Target typedef_explicitly_visible GENPYBIND(visible);
  typedef Target typedef_explicitly_hidden GENPYBIND(hidden);
  typedef Target typedef_implicitly_visible GENPYBIND(opaque(false));

  typedef UnexposedTarget typedef_unexposed_target GENPYBIND(visible);
  typedef DefinedLaterTarget typedef_defined_later_target GENPYBIND(visible);
};

}  // namespace visibility

struct GENPYBIND(visible) DefinedLaterTarget {};
