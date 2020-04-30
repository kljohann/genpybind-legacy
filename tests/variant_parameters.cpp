#include "variant_parameters.h"

std::variant<int, std::string> foo(std::variant<int, std::string> v) {
	return v;
}
