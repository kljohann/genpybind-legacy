#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) has_call {
  int operator()(int value) const;
  int operator()(int first, int second) const;
};

#define TESTCASE_BINARY_OPERATOR(OPNAME, OPERATOR)                             \
  struct GENPYBIND(visible) has_member_##OPNAME {                              \
    bool operator OPERATOR(const has_member_##OPNAME &) const { return true; } \
  };                                                                           \
  struct GENPYBIND(visible) has_non_const_member_##OPNAME {                    \
    bool operator OPERATOR(const has_non_const_member_##OPNAME &) {            \
      return true;                                                             \
    }                                                                          \
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

TESTCASE_BINARY_OPERATOR(sub, -)
TESTCASE_BINARY_OPERATOR(add, +)
TESTCASE_BINARY_OPERATOR(mul, *)
TESTCASE_BINARY_OPERATOR(div, /)
TESTCASE_BINARY_OPERATOR(mod, %)
TESTCASE_BINARY_OPERATOR(lshift, <<)
TESTCASE_BINARY_OPERATOR(rshift, >>)
TESTCASE_BINARY_OPERATOR(and, &)
TESTCASE_BINARY_OPERATOR(or, |)
TESTCASE_BINARY_OPERATOR(xor, ^)
TESTCASE_BINARY_OPERATOR(rsub, -)
TESTCASE_BINARY_OPERATOR(radd, +)
TESTCASE_BINARY_OPERATOR(rmul, *)
TESTCASE_BINARY_OPERATOR(rdiv, /)
TESTCASE_BINARY_OPERATOR(rmod, %)
TESTCASE_BINARY_OPERATOR(rlshift, <<)
TESTCASE_BINARY_OPERATOR(rrshift, >>)
TESTCASE_BINARY_OPERATOR(rand, &)
TESTCASE_BINARY_OPERATOR(ror, |)
TESTCASE_BINARY_OPERATOR(rxor, ^)

#undef TESTCASE_BINARY_OPERATOR

#define TESTCASE_UNARY_OPERATOR(OPNAME, OPERATOR)                              \
  has_unary &operator OPERATOR(int argument) {                                 \
    OPNAME = argument;                                                         \
    return *this;                                                              \
  }                                                                            \
  int OPNAME = 0;

struct GENPYBIND(visible) has_unary {
  TESTCASE_UNARY_OPERATOR(iadd, +=)
  TESTCASE_UNARY_OPERATOR(isub, -=)
  TESTCASE_UNARY_OPERATOR(imul, *=)
  TESTCASE_UNARY_OPERATOR(idiv, /=)
  TESTCASE_UNARY_OPERATOR(imod, %=)
  TESTCASE_UNARY_OPERATOR(ilshift, <<=)
  TESTCASE_UNARY_OPERATOR(irshift, >>=)
  TESTCASE_UNARY_OPERATOR(iand, &=)
  TESTCASE_UNARY_OPERATOR(ior, |=)
  TESTCASE_UNARY_OPERATOR(ixor, ^=)
};

#undef TESTCASE_UNARY_OPERATOR

#define TESTCASE_NULLARY_OPERATOR(OPNAME, OPERATOR)                            \
  has_nullary operator OPERATOR() {                                            \
    has_nullary tmp;                                                           \
    tmp.OPNAME = true;                                                         \
    return tmp;                                                                \
  }                                                                            \
  bool OPNAME = false;

struct GENPYBIND(visible) has_nullary {
  TESTCASE_NULLARY_OPERATOR(neg, -)
  TESTCASE_NULLARY_OPERATOR(pos, +)
  TESTCASE_NULLARY_OPERATOR(invert, ~)
};

#undef TESTCASE_NULLARY_OPERATOR

struct GENPYBIND(visible) has_floordiv {
  // TODO: One should be able to explicitly provide a name for operators.
  // At the moment this leads to the wrapping being handled by the regular
  // method wrapping code.
  GENPYBIND(expose_as(__floordiv__))
  int operator/(int div) const;
};

struct GENPYBIND(visible) has_friend_floordiv {
  // TODO: One should be able to explicitly provide a name for friend
  // operators.  At the moment this does not work yet.
  GENPYBIND(expose_as(__floordiv__))
  friend has_friend_floordiv operator/(const has_friend_floordiv &,
                                       const has_friend_floordiv &) {
    return {};
  }
};
