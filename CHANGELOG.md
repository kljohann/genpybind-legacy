# Change Log

## 0.2.1

### Enhancements

* Snapshot tests based on pydoc have been added.  For each test target, a
  text-only documentation is generated that contains a description of the
  contained modules, classes, functions and methods, their default arguments and
  docstrings etc.  This documentation is compared to artifact files stored in
  [`tests/expected`](./tests/expected).

## 0.2.0

Thanks to several contributors from the [Electronic Vision(s)
Group](https://github.com/electronicvisions) for patches,
documentation and helping to test this release!

### Deprecations

* Support for running genpybind using Python 2.x will likely be dropped in the
  next release.
* Use of the `--genpybind-tag` feature to limit which declarations are exposed
  in a given module will only be allowed on a namespace granularity, by
  applying `tag` or `tags` annotations to namespace definitions.  Definitions
  in nested namespaces will only be exposed if the enclosing namespace is
  exposed.
* The `opaque` keyword will likely be renamed and/or undergo a redesign (see
  [issue 24](https://github.com/kljohann/genpybind/issues/24)).

### Enhancements

* Initial documentation has been added for the genpybind annotations and command
  line arguments.
* It's now possible to specify the [holder
  type](https://pybind11.readthedocs.io/en/stable/advanced/smart_ptrs.html#std-shared-ptr)
  to use for a class using the `holder_type` annotation (see
  [tests/holder_type.h](tests/holder_type.h)).
* A warning is now emitted at import time when a type alias references an
  unknown or unexposed type.
* Type alias declarations are now supported (see [tests/typedefs.h](tests/typedefs.h)).
* `genpybind.h` is now copied to `${PREFIX}/include` when using `./waf
  install`.  It can still be useful to define compatible macros in a consuming
  project instead, in order to use a different name for the macro or allow
  compiling the library without an installed version of genpybind.
* The LLVM patches have been updated to match the LLVM 9.0 release.
* The test suite has been expanded.

### Fixes

* Functions with `pybind::args` or `pybind::kwargs` parameters are now
  wrapped properly.
* Sub-modules are no longer exposed when the enclosing namespace is not exposed.
* Cross-module aliases to nested types are now exposed correctly, as long as
  the referred module is available at runtime.
