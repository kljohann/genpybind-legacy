#pragma once

#include <iostream>

#include "genpybind.h"

#define TESTCASE_INLINEBASE_COMPARE(NAME, OP)                                  \
  friend bool operator OP(const NAME &lhs, const NAME &rhs) {                  \
    return lhs.value() OP rhs.value();                                         \
  }

template <typename Derived> class Base {
public:
  typedef size_t value_type;
  typedef Base<Derived> base_type;

  constexpr explicit Base(const value_type &val = 0) : mValue(val) {}

  constexpr Base(const base_type &) = default;
  base_type &operator=(const base_type &) = default;
  base_type &operator=(const value_type &rhs) {
    mValue = rhs;
    return *this;
  }

  GENPYBIND(expose_as(__int__))
  constexpr operator value_type() const { return mValue; }

  constexpr value_type value() const { return mValue; }

  TESTCASE_INLINEBASE_COMPARE(Derived, ==)
  TESTCASE_INLINEBASE_COMPARE(Derived, !=)
  TESTCASE_INLINEBASE_COMPARE(Derived, <)
  TESTCASE_INLINEBASE_COMPARE(Derived, >)
  TESTCASE_INLINEBASE_COMPARE(Derived, <=)
  TESTCASE_INLINEBASE_COMPARE(Derived, >=)

  GENPYBIND(stringstream)
  friend std::ostream &operator<<(std::ostream &os, const Derived &d) {
    return os << "[" << d.mValue << "]";
  }

  GENPYBIND(expose_as(__hash__))
  size_t hash() const { return mValue; }

private:
  value_type mValue;
};

#undef TESTCASE_INLINEBASE_COMPARE

struct GENPYBIND(inline_base("*Base*")) Enum : public Base<Enum> {
  constexpr explicit Enum(size_t val = 0) : base_type(val) {}
};
