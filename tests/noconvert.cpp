#include "noconvert.h"

bool called_with_double(double value) { return true; }
bool called_with_double(int value) { return false; }
double convert(double value) { return value; }
double noconvert(double value) { return value; }
double noconvert_first(double first, double second) { return first + second; }
double noconvert_numeric(double first, double second) { return first + second; }
