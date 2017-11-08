#pragma once

#include "genpybind.h"

namespace submodule GENPYBIND(module) {
class GENPYBIND(visible) X {};
} // namespace submodule

namespace submodule_ GENPYBIND(visible, module) {
class X {};
} // namespace submodule_

namespace submodule_named GENPYBIND(visible, module(named)) {
class X {};
} // namespace submodule_named

namespace submodule_expose_as GENPYBIND(visible, module, expose_as(expose_as)) {
class X {};
} // namespace submodule_expose_as

namespace submodule_named_expose_as GENPYBIND(visible, module(xyz), expose_as(ignored)) {
class X {};
} // namespace submodule_named_expose_as
