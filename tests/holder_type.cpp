#include "holder_type.h"

std::shared_ptr<Child> Parent::get_child() { return child; }

long Parent::get_use_count() { return child.use_count(); }
