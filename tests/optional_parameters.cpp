#include "optional_parameters.h"

std::optional<int> GENPYBIND(visible) foo(std::optional<int> o) { return o; }
