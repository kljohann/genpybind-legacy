#pragma once

#include <memory>

#include "genpybind.h"

class GENPYBIND(visible, holder_type("std::shared_ptr<Child>")) Child
    : public std::enable_shared_from_this<Child> {};

class GENPYBIND(visible) Parent {
public:
  Parent() : child(std::make_shared<Child>()) {}
  std::shared_ptr<Child> get_child();
  long get_use_count();

private:
  std::shared_ptr<Child> child;
};
