#pragma once

#include <utility>
#include <tuple>

#include "genpybind.h"

#ifdef GENPYBIND
// FIXME: this is ugly
#include <pybind11/pybind11.h>
PYBIND11_MAKE_OPAQUE(std::pair<float, float>);
#endif 

template class std::pair<float, float>;

typedef std::pair<float, float>  my_float_pair GENPYBIND(opaque);

std::pair<float, float> GENPYBIND(visible) generate_float_pair()
{
	return std::make_pair(0.1, 1.1);
}
