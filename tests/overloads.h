#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Something {
  Something() = default;
  Something(int arg);
  Something(int first, int second);

  void set();
  void set(int arg);
  void set(int first, int second);

  int value = 0;
};

int GENPYBIND(visible) overloaded(int arg);
int GENPYBIND(visible) overloaded(int first, int second);
