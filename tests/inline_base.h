#pragma once

#include "genpybind.h"

// FIXME: inline_base may need PR 855 / pybind11 2.2.0 to work ?

struct Base {
  int member_function() const;
};

struct GENPYBIND(inline_base("::Base")) Derived : public Base {};

class GENPYBIND(visible) OtherBase {
public:
  bool from_other_base() const;
};

struct GENPYBIND(inline_base("::Base")) DerivedMultiple : public Base,
                                                          public OtherBase {};

struct GENPYBIND(visible) DerivedDerived : public Derived {};

struct GENPYBIND(visible) DerivedDerivedMultiple : public Derived,
                                                   public OtherBase {};

struct Indirect : public Base {
  bool from_indirect() const;
};

struct GENPYBIND(inline_base("::Indirect", "::Base")) DerivedIndirect
    : public Indirect {};

// inline_base attribute has no effect as no further processing is done because
// "Indirect" base is hidden.
struct GENPYBIND(hide_base("::Indirect"), inline_base("::Base")) DerivedHide
    : public Indirect {};

// TODO: Add more complex match expressions
