#pragma once

#include "genpybind.h"

class GENPYBIND(visible) Something {
public:
  GENPYBIND(getter_for(value))
  int get_value() const;

  GENPYBIND(setter_for(value))
  void set_value(int value);

  GENPYBIND(getter_for(readonly))
  bool computed() const;

  GENPYBIND(accessor_for(other, get))
  int get_other() const;

  GENPYBIND(accessor_for(other, set))
  void set_other(int value);

private:
  int m_value = 0;
  int m_other = 0;
};
