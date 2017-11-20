#pragma once

#include <iostream>

#include "genpybind.h"

struct GENPYBIND(visible) Something {
  GENPYBIND(stringstream)
  friend std::ostream &operator<<(std::ostream &os, const Something &) {
    return os << "uiae";
  }
};
