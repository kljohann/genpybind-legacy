#include <pybind11/pybind11.h>

#include "argsandkwargs.h"

int test_args(pybind11::args args) {
	return pybind11::len(args);
}

int test_kwargs(pybind11::kwargs kwargs) {
	size_t ret = 0;
	for (auto const& elem: kwargs)
		ret += pybind11::len(elem.second);
	return ret;
}

int test(pybind11::args args) {
	return test_args(args);
}

int test(pybind11::kwargs kwargs) {
	return test_kwargs(kwargs);
}

int test(int i, float f, pybind11::args args) {
	return test_args(args);
}

int test(int i, float f, pybind11::kwargs kwargs) {
	return test_kwargs(kwargs);
}

int test(int i, float f, pybind11::args args, pybind11::kwargs kwargs) {
	return test_args(args) + test_kwargs(kwargs);
}
