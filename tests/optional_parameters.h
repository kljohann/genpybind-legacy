#pragma once

#if !__has_include("optional")
#include <experimental/optional>
namespace std {
template<typename T>
using optional = std::experimental::optional<T>;
using nullopt_t = std::experimental::nullopt_t;
using std::experimental::nullopt;
}
#else
#include <optional>
#endif

#include "genpybind.h"

std::optional<int> GENPYBIND(visible) foo(std::optional<int> o = std::nullopt);
