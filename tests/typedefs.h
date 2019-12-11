#pragma once

#include "genpybind.h"

// TODO: Add tests for opaque typedefs, (non-)alias typedefs

struct GENPYBIND(visible) Target {};

namespace visibility {

// Typedefs have to be made visible explicitly.
typedef Target typedef_not_visible;
typedef Target typedef_explicitly_visible GENPYBIND(visible);
typedef Target typedef_explicitly_hidden GENPYBIND(hidden);
typedef Target typedef_implicitly_visible GENPYBIND(opaque(false));

struct GENPYBIND(visible) VisibleParent {
  typedef Target typedef_not_visible;
  typedef Target typedef_explicitly_visible GENPYBIND(visible);
  typedef Target typedef_explicitly_hidden GENPYBIND(hidden);
  typedef Target typedef_implicitly_visible GENPYBIND(opaque(false));
};

}  // namespace visibility
