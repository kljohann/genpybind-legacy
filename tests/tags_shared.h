#pragma once

#include "genpybind.h"

class GENPYBIND(visible) Everywhere {};
class GENPYBIND(tag(tags_a)) OnlyInA {};
class GENPYBIND(tag(tags_b)) OnlyInB {};
class GENPYBIND(tag(tags_a, tags_b)) OnlyInAB {};
class GENPYBIND(tag(all_tests)) EverywhereInTests {};

#define GENPYBIND_ONLY_IN_AB GENPYBIND(tags(tags_a, tags_b))
#define GENPYBIND_MODULE GENPYBIND(module)

namespace ab GENPYBIND_ONLY_IN_AB {
namespace NestedSubmoduleOnlyInAB GENPYBIND_MODULE {
class GENPYBIND(visible) X {};
// Even though we specified the tag for all tests, this will only be exposed in
// A and B, because the submodule is only exposed in A and B.
class GENPYBIND(visible, tag(all_tests)) AlsoOnlyInAB {};
} // namespace NestedSubmoduleOnlyInAB

class GENPYBIND(visible) NamespacedOnlyInAB {};
} // namespace ab

namespace ab {
class GENPYBIND(visible) NamespacedEverywhere {};
} // namespace ab
