#pragma once

#if !__has_include("variant")
#include <experimental/variant>
namespace std {
template<typename T>
using variant = std::experimental::variant<T>;
}
#else
#include <variant>
#endif

#include "genpybind.h"

#include <string>

std::variant<int, std::string> GENPYBIND(visible) foo(std::variant<int, std::string>);
