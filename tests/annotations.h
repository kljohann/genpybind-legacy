#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Plain {};

struct GENPYBIND(visible()) AsCall {};

struct GENPYBIND(visible(true)) WithArgTrue {
  int with_arg_default GENPYBIND(visible(default));
  int with_arg_false GENPYBIND(visible(false));
  int with_arg_none GENPYBIND(visible(none));
};

struct GENPYBIND(visible(True)) WithPythonSpelling {
  int with_arg_false GENPYBIND(visible(False));
  int with_arg_none GENPYBIND(visible(None));
};


GENPYBIND(noconvert(first, "second", 2))
double multiple_mixed_args(double first, double second, double third);
