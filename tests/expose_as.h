#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) X {
  int xfield;
};

struct Y {
  int yfield = 42;
};

enum class GENPYBIND(expose_as("enum")) some_enum { A, B, C };

extern X const x GENPYBIND(expose_as(x_instance));

class GENPYBIND(visible, expose_as(Dummy)) dummy {
public:
  dummy(int value);

  typedef X type GENPYBIND(expose_as("typedef"));

  static bool function() GENPYBIND(expose_as("static"));

  GENPYBIND(expose_as(constant_))
  static constexpr bool constant = true;

  bool member GENPYBIND(expose_as(member_));

  GENPYBIND(expose_as(__hash__))
  int hash() const;

  GENPYBIND(expose_as(__int__))
  operator int() const;

  typedef Y y_type GENPYBIND(opaque, expose_as("y_type_"));

private:
  int m_value;
};

GENPYBIND(visible, expose_as(free_function_))
void free_function();
