#include "overloads.h"

Something::Something(int arg) : value(arg) {}
Something::Something(int first, int second) : value(first + second) {}

void Something::set() { value = 0; }
void Something::set(int arg) { value = arg; }
void Something::set(int first, int second) { value = first + second; }

int overloaded(int arg) { return arg; }
int overloaded(int first, int second) { return first + second; }
