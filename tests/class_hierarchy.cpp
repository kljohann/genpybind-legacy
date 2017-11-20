#include "class_hierarchy.h"

bool Base::from_base() const { return true; }
bool Base::overloaded(int value) const { return true; }
bool Base::overloaded(int first, int second) const { return true; }

bool DerivedPublic::overloaded(int value) const { return false; }

bool DerivedPrivate::overloaded(int value) const { return false; }

bool DerivedInline::overloaded(int value) const { return false; }

bool OtherBase::from_other_base() const { return true; }
