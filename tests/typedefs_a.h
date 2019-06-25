#pragma once

#include "genpybind.h"
#include "typedefs_b.h"

// TODO: Add tests for opaque typedefs, (non-)alias typedefs

class GENPYBIND(visible) A {};

typedef A typedef_A GENPYBIND(visible);

GENPYBIND_MANUAL({
	parent->py::module::import("pytypedefs_b");
})

typedef b::B typedef_B GENPYBIND(visible);
