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

// FIXME: This is inconsistent with the keep_alive notation.  Consider dropping
// support for numeric arguments in both cases.
GENPYBIND(noconvert(0, 1))
double noconvert_numeric(double first, double second);
