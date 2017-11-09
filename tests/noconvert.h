#pragma once

#include "genpybind.h"

GENPYBIND(visible)
bool called_with_double(double value);

GENPYBIND(visible)
bool called_with_double(int value);

GENPYBIND(visible)
double convert(double value);

GENPYBIND(noconvert(value))
double noconvert(double value);

GENPYBIND(noconvert(first))
double noconvert_first(double first, double second);
