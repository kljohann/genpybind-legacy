#include "abstract_base.h"

int AbstractBase::whatever(int value) const { return value; }
int AbstractBase::something(int value) const { return value; }

bool AbstractBase::static_method() { return true; }

int Derived::something(int value) const { return -value; }
double Derived::return_magic_number() const { return 42.0; }
