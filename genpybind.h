#pragma once

#ifdef __GENPYBIND__
#define GENPYBIND_PARENT_TYPE auto
#define GENPYBIND__CONCAT_(x, y) x##y
#define GENPYBIND__CONCAT(x, y) GENPYBIND__CONCAT_(x, y)
#define GENPYBIND__MAKE_UNIQUE(x) GENPYBIND__CONCAT(x, __COUNTER__)
#define GENPYBIND(...) __attribute__((annotate("◊" #__VA_ARGS__)))
// Will not be included in binary, because it is an uninstantiated template due to auto& parameter.
// Note: This needs C++17 during genpybind run, as lambda closure types are non-literal types
//       before C++17 and thus cannot be constexpr.
#define GENPYBIND__MANUAL_(...)                                                                    \
	static constexpr auto __attribute__((unused)) GENPYBIND(manual)                                \
		GENPYBIND__MAKE_UNIQUE(genpybind_) = [](auto& parent) __VA_ARGS__;
#define GENPYBIND_MANUAL GENPYBIND__MANUAL_
#else
#define GENPYBIND(...)
#define GENPYBIND_MANUAL(...)
#endif // __GENPYBIND__
