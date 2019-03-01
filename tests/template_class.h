#pragma once

#include <array>
#include "genpybind.h"

namespace somewhere {

	template<typename T>
struct TBase {
	constexpr static unsigned num_words = 1;

	std::array<int, num_words> do_something() { return {}; }
};

} // namespace somewhere

template class somewhere::TBase<int>;

GENPYBIND(opaque)
typedef somewhere::TBase<int> TBase_int;
