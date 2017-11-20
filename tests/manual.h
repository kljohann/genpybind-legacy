#pragma once

#include "genpybind.h"

namespace something {

class GENPYBIND(visible) Something {
public:
  bool whatever() const;

  GENPYBIND_MANUAL({
    // FIXME: &Something::whatever does not work
    parent.def("something", &::something::Something::whatever);
    parent.def("__getitem__",
               [](GENPYBIND_PARENT_TYPE &self, int key) { return key; });
  })
};

} // namespace something

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
