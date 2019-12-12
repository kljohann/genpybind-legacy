#pragma once

#include "genpybind.h"

class GENPYBIND(visible) Argument {};

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

  GENPYBIND(getter_for(overloaded))
  int get_overloaded() const;

  GENPYBIND(hidden)
  int get_overloaded(Argument ignored) const;

  GENPYBIND(setter_for(overloaded))
  void set_overloaded(int value);

  GENPYBIND(hidden)
  void set_overloaded(Argument ignored);

private:
  int m_value = 0;
  int m_other = 0;
  int m_overloaded = 0;
};
