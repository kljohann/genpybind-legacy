#pragma once

#include "genpybind.h"

// TODO: Add check for other operators, unary operators, ...

// TODO: Add check for non-const member function operators

#define TESTCASE_BINARY_OPERATOR(OPNAME, OPERATOR)                             \
  struct GENPYBIND(visible) has_member_##OPNAME {                              \
    bool operator OPERATOR(const has_member_##OPNAME &) const { return true; } \
  };                                                                           \
  struct GENPYBIND(visible) has_private_##OPNAME {                             \
  private:                                                                     \
    bool operator OPERATOR(const has_private_##OPNAME &) const {               \
      return true;                                                             \
    }                                                                          \
  };                                                                           \
  struct GENPYBIND(visible) has_hidden_##OPNAME {                              \
    GENPYBIND(hidden)                                                          \
    bool operator OPERATOR(const has_hidden_##OPNAME &) const { return true; } \
  };                                                                           \
  struct GENPYBIND(visible) has_friend_##OPNAME {                              \
    friend bool operator OPERATOR(const has_friend_##OPNAME &,                 \
                                  const has_friend_##OPNAME &) {               \
      return true;                                                             \
    }                                                                          \
  };                                                                           \
  struct GENPYBIND(visible) has_hidden_friend_##OPNAME {                       \
    friend bool operator OPERATOR(const has_hidden_friend_##OPNAME &,          \
                                  const has_hidden_friend_##OPNAME &)          \
        GENPYBIND(hidden) {                                                    \
      return true;                                                             \
    }                                                                          \
  };

TESTCASE_BINARY_OPERATOR(lt, <)
TESTCASE_BINARY_OPERATOR(le, <=)
TESTCASE_BINARY_OPERATOR(eq, ==)
TESTCASE_BINARY_OPERATOR(ne, !=)
TESTCASE_BINARY_OPERATOR(gt, >)
TESTCASE_BINARY_OPERATOR(ge, >=)

#undef TESTCASE_BINARY_OPERATOR
