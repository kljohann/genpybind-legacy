#include "explicit_template_function.h"

template <typename T> T Klass::increase(const T &val) { return val + 1; }

template <typename T> T frobnicate(const T &val) { return 42 - val; }

template int Klass::increase(const int &);
template int frobnicate<int>(const int &);
template double frobnicate<double>(const double &);
