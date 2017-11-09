#pragma once

#include "genpybind.h"

struct noncopyable {
  noncopyable() = default;
  ~noncopyable() = default;
  noncopyable(const noncopyable &) = delete;
  noncopyable &operator=(const noncopyable &) = delete;
};

struct Unexposed {
  int unexposed_base_field = 5;
};

struct GENPYBIND(visible) Exposed {
  int exposed_base_field = 5;
};

struct GENPYBIND(visible) PrivateBase : private noncopyable {};

// This does not work:
//   struct GENPYBIND(visible) UnexposedBase : public Unexposed {};
// => type "UnexposedBase" referenced unknown base type "Unexposed"

struct GENPYBIND(visible) ExposedBase : public Exposed {};

struct GENPYBIND(hide_base("*Unexposed")) HiddenUnexposedBase
    : public Unexposed {};

struct GENPYBIND(hide_base("*Exposed")) HiddenExposedBase : public Exposed {};
