#include "keep_alive.h"

Child::Child() { ++created; }
Child::~Child() { ++destroyed; }
int Child::created = 0;
int Child::destroyed = 0;

Parent::Parent() { ++created; }
Parent::~Parent() { ++destroyed; }
int Parent::created = 0;
int Parent::destroyed = 0;

Parent::Parent(Child *child) : Parent() {}

void Parent::sink(Child *child) {}
void Parent::sink_keep_alive(Child *child) {}
void Parent::sink_keep_alive_plain(Child *child) {}

Child *Parent::source() { return new Child(); }
Child *Parent::source_keep_alive() { return new Child(); }
Child *Parent::source_keep_alive_parent() { return new Child(); }
