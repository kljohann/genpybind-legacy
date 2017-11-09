#pragma once

#include "genpybind.h"

#define GENPYBIND_TEST_MEMBERS                                                 \
  static int static_field;                                                     \
  static const int static_const_field = 2;                                     \
  static constexpr int static_constexpr_field = 3;                             \
  GENPYBIND(readonly)                                                          \
  static int static_readonly_field;                                            \
  GENPYBIND(writable(false))                                                   \
  static int static_writable_false_field;                                      \
                                                                               \
  int field = 1;                                                               \
  const int const_field = 2;                                                   \
  GENPYBIND(readonly)                                                          \
  int readonly_field = 4;                                                      \
  GENPYBIND(writable(false))                                                   \
  int writable_false_field = 5;

struct GENPYBIND(visible) SomeStruct {
  GENPYBIND_TEST_MEMBERS
};

class GENPYBIND(visible) SomeClass {
public:
  GENPYBIND_TEST_MEMBERS
};

#undef GENPYBIND_TEST_MEMBERS

extern int var GENPYBIND(visible);
extern const int const_var GENPYBIND(visible);
