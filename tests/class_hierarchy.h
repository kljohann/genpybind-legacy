#pragma once

#include "genpybind.h"

// TODO: check for all declaration types that inline_base of an exposed base does not
// lead to "already registered" errors

class GENPYBIND(visible) Base {
public:
  int base_field = 0;
  bool from_base() const;
  bool overloaded(int value) const;
  bool overloaded(int first, int second) const;
};

class GENPYBIND(visible) DerivedPublic : public Base {
public:
  bool overloaded(int value) const;
};

class GENPYBIND(visible) DerivedPrivate : private Base {
public:
  bool overloaded(int value) const;
};

class GENPYBIND(inline_base("*Base")) DerivedInline : public Base {
public:
  bool overloaded(int value) const;
};

class GENPYBIND(visible) OtherBase {
public:
  bool from_other_base() const;
};

class GENPYBIND(visible) DerivedMultiple : public Base, public OtherBase {};
