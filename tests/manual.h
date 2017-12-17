#pragma once

#include <iostream>

#include "genpybind.h"

namespace something {

class GENPYBIND(visible) Something {
public:
  bool whatever() const;

  GENPYBIND(hidden)
  friend std::ostream &operator<<(std::ostream &os, const Something &) {
    return os << "uiae";
  }

  int offset = 5;

  GENPYBIND_MANUAL({
    // FIXME: &Something::whatever does not work
    parent.def("something", &::something::Something::whatever);
    // ==> genpybind_class_decl__something_Something_Something.def(
    // ==>     "something", &::something::Something::whatever);

    // We need to use the special macro GENPYBIND_PARENT_TYPE since the class itself is
    // not complete at this point.  (This macro uses `auto` to turn the lambda into a
    // generic lambda during parsing of the GENPYBIND_MANUAL expression.  It will be
    // replaced by the real type in the generated bindings.)
    parent.def("__getitem__", [](GENPYBIND_PARENT_TYPE &self, int key) {
      return self.offset + key;
    });
    // ==> genpybind_class_decl__something_Something_Something.def(
    // ==>     "__getitem__", [](::something::Something &self, int key) {
    // ==>       return self.offset + key;
    // ==>     });

    // Note the convoluted syntax necessary for writing a call to a template function:
    parent.def(
        "__str__",
        parent->template genpybind_stringstream_helper<::something::Something>());
    // ==> genpybind_class_decl__something_Something_Something.def(
    // ==>     "__str__", genpybind_stringstream_helper<::something::Something>());
  })
};

} // namespace something

// Unscoped GENPYBIND_MANUAL macros can be used to add preamble and postamble code to the
// generated bindings, e.g. for importing required libraries or executing python code that
// dynamically patches the generated bindings.

GENPYBIND(postamble)
GENPYBIND_MANUAL({
  auto env = parent->py::module::import("os").attr("environ");
  // should not have any effect as this will be run after preamble code
  env.attr("setdefault")("genpybind", "postamble");
  env.attr("setdefault")("genpybind_post", "postamble");
})

GENPYBIND_MANUAL({
  auto env = parent->py::module::import("os").attr("environ");
  env.attr("setdefault")("genpybind", "preamble");
})
