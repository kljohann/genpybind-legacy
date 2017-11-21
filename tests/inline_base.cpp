#include "inline_base.h"

int Base::member_function() const { return 42; }

bool OtherBase::from_other_base() const { return true; }

bool Indirect::from_indirect() const { return true; }
