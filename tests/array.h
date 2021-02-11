#pragma once

#include <array>

#include "genpybind.h"

struct GENPYBIND(hidden) Something : public std::array<float, 10>
{};

#ifdef GENPYBIND
#include <pybind11/stl_bind.h>
// TODO: replace by pybind11::bind_array as soon as available :p
GENPYBIND_MANUAL({
	pybind11::class_<Something>(parent, "Something")
		.def(pybind11::init<>())
		.def("__len__", [](Something const& v) { return v.size(); })
		.def("__iter__", [](Something& v) {
		return pybind11::make_iterator(std::begin(v), std::end(v));
		}, pybind11::keep_alive<0, 1>())
		.def("__getitem__", [](Something const& v, size_t const i) -> float {
			return v[i];
		})
		.def("__setitem__", [](Something& v, size_t const i, float const& val) {
			v[i] = val;
		})
	;
})
#endif
