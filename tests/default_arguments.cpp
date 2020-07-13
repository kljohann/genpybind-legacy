#include "default_arguments.h"

constexpr int example::Y::N;

template <typename T> T template_function_with_default(T value) {
  return value;
}

template int template_function_with_default<int>(int);

template <typename T> T template_function_with_default_from_function(T value) {
  return value;
}

template int template_function_with_default_from_function<int>(int);

template struct HasMemberFunctionWithDefaultArguments<void>;

// template <typename T>
// int template_function_with_dependant_default(T /*ignore*/, int value) {
//   return value;
// }

// template int
// template_function_with_dependant_default<DefaultValue>(DefaultValue, int);

// template <typename T>
// int template_function_with_dependant_default_from_function(T /*ignore*/, int value) {
//   return value;
// }

// template int
// template_function_with_dependant_default_from_function<DefaultValue>(DefaultValue, int);
