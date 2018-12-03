#pragma once

#include <string>

#include "genpybind.h"

namespace pybind11 {
class args;
class kwargs;
}

#define SYMBOL_VISIBLE __attribute__((visibility("default")))

GENPYBIND(visible) SYMBOL_VISIBLE
int test_args(pybind11::args args);

GENPYBIND(visible) SYMBOL_VISIBLE
int test_kwargs(pybind11::kwargs kwargs);

GENPYBIND(visible) SYMBOL_VISIBLE
int test(pybind11::args args);

GENPYBIND(visible) SYMBOL_VISIBLE
int test(pybind11::kwargs kwargs);

GENPYBIND(visible) SYMBOL_VISIBLE
int test(int i, float f, pybind11::args args);

GENPYBIND(visible) SYMBOL_VISIBLE
int test(int i, float f, pybind11::kwargs kwargs);

GENPYBIND(visible) SYMBOL_VISIBLE
int test(int i, float f, pybind11::args args, pybind11::kwargs kwargs);
