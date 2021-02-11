#include "default_arguments.h"

constexpr int example::Y::N;

template <typename T>
int function_templated(T o) { return o; }

template GENPYBIND(visible) int function_templated<int>(int o = 42);
