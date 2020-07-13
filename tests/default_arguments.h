#pragma once

#include "genpybind.h"

template <typename T, int N> struct Tpl {};

struct GENPYBIND(visible) X {};

void GENPYBIND(visible) function_builtin(int x = 5, bool arg = true) {}
void GENPYBIND(visible) function_class(X x = X()) {}

namespace example {
struct GENPYBIND(visible) Y {
  static constexpr int N = 42;
};
void GENPYBIND(visible) function_class_in_namespace(Y y = Y()) {}
} // namespace example

void GENPYBIND(visible)
    function_class_outside_namespace(example::Y y = example::Y()) {}

// TODO: genpybind uses `example::Y::N` as default argument?
/*
void GENPYBIND(visible) function_template_outside_namespace(
    Tpl<example::Y, example::Y::N> y = Tpl<example::Y, example::Y::N>()) {}
*/

// TODO: genpybind fails to expand `Y::N` to fully qualified expression
/*
namespace example {
void GENPYBIND(visible)
    function_template_in_namespace(Tpl<Y, Y::N> y = Tpl<Y, Y::N>()) {}
} // namespace example
*/

// TODO: braced initialization not supported in default argument
/*
void GENPYBIND(visible) function_braced(X x = {}) {}
namespace example {
void GENPYBIND(visible) function_braced_in_namespace(Y y = {}) {}
} // namespace example
void GENPYBIND(visible) function_braced_outside_namespace(example::Y y = {})
*/

template <typename T>
T template_function_with_default(T value = 42) GENPYBIND(visible);

extern template int template_function_with_default<int>(int);

constexpr int foo() { return 23; }

template <typename T>
T template_function_with_default_from_function(T value = foo())
    GENPYBIND(visible);

extern template int template_function_with_default_from_function<int>(int);

template <typename T>
struct GENPYBIND(visible) HasMemberFunctionWithDefaultArguments {
  int identity(int value = 42) { return value; }
};

extern template struct HasMemberFunctionWithDefaultArguments<void>;

struct GENPYBIND(visible) DefaultValue {
  static constexpr int value = 123;

  static constexpr int foo() { return 23; }
};

// FIXME: This does not work, as expression is not properly resolved:
// `::DefaultValue::T::value` instead of `::DefaultValue::value`.

// template <typename T>
// int template_function_with_dependant_default(T ignore, int value = T::value)
//     GENPYBIND(visible);

// extern template int
// template_function_with_dependant_default<DefaultValue>(DefaultValue, int);

// template <typename T>
// int template_function_with_dependant_default_from_function(T ignore,
//                                                            int value = T::foo())
//     GENPYBIND(visible);

// extern template int
// template_function_with_dependant_default_from_function<DefaultValue>(
//     DefaultValue, int);
