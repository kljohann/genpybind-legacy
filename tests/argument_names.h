#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Something {
  Something(int first, bool second, long third = 5);

  void do_something(int some_argument, double another_argument);
};

GENPYBIND(visible)
bool some_function(bool option, bool something = true);
