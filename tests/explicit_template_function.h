#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Something {
  Something() = default;
  template <typename T> Something(T val);
  int value = 0;
};

struct GENPYBIND(visible) Klass {
  template <typename T> T increase(const T &val) GENPYBIND(visible);
}; // Klass

template <typename T> T frobnicate(const T &val) GENPYBIND(visible);

extern template Something::Something(int);
extern template int Klass::increase(const int &);
extern template int frobnicate<int>(const int &);
extern template double frobnicate<double>(const double &);
