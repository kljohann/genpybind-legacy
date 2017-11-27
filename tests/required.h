#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Child {};

struct GENPYBIND(visible) Parent {
  void accept(Child *child);

  GENPYBIND(required(child))
  void required(Child *child);
};
