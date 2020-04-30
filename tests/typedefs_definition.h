#pragma once

#include "genpybind.h"

// The types inside this namespace are only exposed in this module, not when the
// header is transitively included elsewhere.  See `typedefs_across_modules.h`
// for the place where this is used.

namespace definition GENPYBIND(tag(typedefs_definition)) {

struct GENPYBIND(visible) Definition {
  struct NestedDefinition {};
  typedef NestedDefinition NestedTypedef GENPYBIND(visible);
};

typedef Definition Typedef GENPYBIND(visible);

} // namespace definition
