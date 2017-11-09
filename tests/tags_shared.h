#pragma once

#include "genpybind.h"

class GENPYBIND(visible) Everywhere {};
class GENPYBIND(tag(tags_a)) OnlyInA {};
class GENPYBIND(tag(tags_b)) OnlyInB {};
class GENPYBIND(tag(tags_a, tags_b)) OnlyInAB {};
class GENPYBIND(tag(all_tests)) EverywhereInTests {};

namespace ab GENPYBIND(tags(tags_a, tags_b)) {
class GENPYBIND(visible) NamespacedOnlyInAB {};
} // namespace ab

namespace ab {
class GENPYBIND(visible) NamespacedEverywhere {};
} // namespace ab

