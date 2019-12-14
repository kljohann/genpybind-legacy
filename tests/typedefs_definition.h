#pragma once

#include "genpybind.h"

// This type is only exposed in this module, not when the header is
// transitively included elsewhere.  See `typedefs_across_modules.h`
// for the place where this is used.
namespace definition GENPYBIND(tag(typedefs_definition)) {
class GENPYBIND(visible) Definition {};
typedef Definition Typedef GENPYBIND(visible);
} // namespace definition
