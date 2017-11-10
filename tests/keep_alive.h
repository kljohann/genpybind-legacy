#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) Child {
  Child();
  ~Child();

  GENPYBIND(readonly)
  static int created;
  GENPYBIND(readonly)
  static int destroyed;
};

struct GENPYBIND(visible) Parent {
  Parent();
  ~Parent();

  GENPYBIND(readonly)
  static int created;
  GENPYBIND(readonly)
  static int destroyed;

  GENPYBIND(keep_alive(this, child))
  Parent(Child *child);

  void sink(Child *child);

  GENPYBIND(keep_alive(this, child))
  void sink_keep_alive(Child *child);

  GENPYBIND(keep_alive(1, 2))
  void sink_keep_alive_plain(Child *child);

  Child *source();

  GENPYBIND(keep_alive(this, "return"))
  Child *source_keep_alive();

  GENPYBIND(keep_alive("return", this))
  Child *source_keep_alive_parent();
};
