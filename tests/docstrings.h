#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Something {
  /// \brief The default constructor!
  /// More documentation here.
  Something() = default;

  /// \brief A member function!
  /// More documentation here.
  void do_something() {}

  /// \brief A comparison operator!
  /// More documentation here.
  bool operator==(Something const &/*other*/) const { return true; }

  /// \brief Inline friend!
  /// More documentation here.
  friend bool operator!=(Something const &/*lhs*/, Something const &/*rhs*/) {
    return false;
  }

  friend bool operator<(Something const &lhs, Something const &rhs);
};

/// \brief Less than!
/// More documentation here.
bool operator<(Something const & /*lhs*/, Something const & /*rhs*/) {
  return false;
}

/// \brief A free function!
/// More documentation here.
GENPYBIND(visible)
void some_function() {}
