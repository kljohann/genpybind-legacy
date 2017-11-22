# genpybind

*Autogeneration of Python bindings from manually annotated C++ headers*

`genpybind` is a tool based on [clang][clang], which automatically generates the code which is
necessary to expose a C++ API as a Python extension via [pybind11][pybind11].
To reduce the complexity and required heuristics, it relies on additional manual hints that are
added to the header file in the form of unobtrusive annotation macros[^1].
While this mandates that you are able to change the actual interface declaration, it results in
a succinct file that describes both the C++ and Python interface of your library.  However, as a
consequence, manually writing pybind11 code is still necessary for code which is not under your
control.

That said, a simple class that should be exposed via a Python extension could look as follows:

```cpp
#pragma once

#include "genpybind.h"

class GENPYBIND(visible) Example {
public:
  static constexpr int GENPYBIND(hidden) not_exposed = 10;

  /// \brief Do a complicated calculation.
  int calculate(int some_argument = 5) const;

  GENPYBIND(getter_for(something))
  int getSomething() const;

  GENPYBIND(setter_for(something))
  void setSomething(int value);

private:
  int _value = 0;
};
```

The resulting extension can then be used like this:

```python
>>> import pyexample as m
>>> obj = m.Example()
>>> obj.something
0
>>> obj.something = 42
>>> obj.something
42
>>> obj.calculate() # default argument
47
>>> obj.calculate(2)
44
>>> help(obj.calculate)
Help on method calculate in module pyexample:

calculate(...) method of pyexample.Example instance
    calculate(self: pyexample.Example, some_argument: int=5) -> int

    Do a complicated calculation.
```

As you can see, annotations are included inline to control what is exposed to the Python extension,
whether getters or setters are exposed as a class property, ….
The resulting Python extension will among other things include docstrings, argument names and
default arguments for functions.  Imagine how much time you will save by not manually keeping the
python bindings and header files in sync! For the example presented above `genpybind` will generate
the following:

```cpp
auto genpybind_class_decl__Example_Example =
    py::class_<::Example>(m, "Example");

{
  typedef int (::Example::*genpybind_calculate_type)(int) const;
  genpybind_class_decl__Example_Example.def(
      "calculate", (genpybind_calculate_type) & ::Example::calculate,
      "Do a complicated calculation.", py::arg("some_argument") = 5);
}
genpybind_class_decl__Example_Example.def(py::init<>(), "");
genpybind_class_decl__Example_Example.def(py::init<const ::Example &>(), "");
genpybind_class_decl__Example_Example.def_property(
    "something", py::cpp_function(&::Example::getSomething),
    py::cpp_function(&::Example::setSomething));
```

# Implementation

The current implementation was started as a proof-of-concept to see whether the described approach
was viable for an existing code base.  Due to its prototypical and initially fast-changing nature
it was based off the `libclang` bindings.  However, as of clang 5.0.0 not all necessary information
was available via this API.  (For example, implicitly instantiated constructors are not exposed.)
To work around this issue, several patches on top of libclang are included in this repository (some
of them have already been merged upstream; some are rather hacky or not yet finished/fully tested).
In addition, a `genpybind-parse` tool based on the internal libtooling clang API is used to
extend/amend the abstract syntax tree (e.g. instantiate implicit member functions) and store it in
a temporary file.  This file is then read by the Python-based tool via the patched `libclang` API.

Evidently, now that the approach has been shown to work, the implementation could transition to be
a single C++ tool based on the internal `libtooling` API.  I eventually plan to go down that road.

## Known defects and shortcomings

- Documentation is non-existent at the moment.  If you want to look at example use-cases the
  [integration tests](./tests) might provide a starting point.
- Expressions and types in default arguments, return values or `GENPYBIND_MANUAL` instructions are
  not consistently expanded to their fully qualified form.  As a workaround it is suggested to use
  the fully-qualified name where necessary.

# Installation

1. Build and install llvm/clang 5.0.0 with the provided patches.  You can use a different prefix
   when installing, to prevent the patched clang from interfering with the version provided by your
   distribution.
   Let's assume you unpacked the source code to `$HOME/llvm-src` and used
   `-DCMAKE_INSTALL_PREFIX=$HOME/llvm`.
2. Make sure genpybind can find the the libclang Python bindings:
   ```bash
   export PYTHONPATH=$HOME/llvm-src/tools/clang/bindings/python \
     LD_LIBRARY_PATH=$HOME/llvm/lib
   ```
3. Build the `genpybind-parse` executable:
   ```bash
   PYTHON=/usr/bin/python2 CXX=/bin/clang++ CC=/bin/clang \
     LLVM_CONFIG=$HOME/llvm/bin/llvm-config \
     ./waf configure --disable-tests
   ./waf build
   ```
   Note that custom Python/compiler/llvm-config executables can be provided via environment
   variables.  If you happened to use the `-DBUILD_SHARED_LIBS=ON` option when building clang you
   need to pass `--clang-use-shared` to `waf configure`.

   **Optional:** If you want to build and run the integration tests you need to install [pytest][pytest]
   and [pybind11][pybind11] and should remove the `--disable-tests` argument to `waf configure`.
   You can use the `--pybind11-includes` option to point to the include path required for pybind11.
4. Install the genpybind tool:
   ```bash
   ./waf install
   ```
   By default genpybind will be installed to `/usr/local/`.  Use the `--prefix` argument of `waf
   configure` if you prefer a different location.
5. Create Python bindings from your C++ header files:
   ```bash
   # Remember to set up your environment as done in step 2 each time you run genpybind:
   export PYTHONPATH=$HOME/llvm-src/tools/clang/bindings/python \
     LD_LIBRARY_PATH=$HOME/llvm/lib
   # The following assumes that both `genpybind` and `genpybind-parse` are on your path.
   genpybind --genpybind-module pyexample --genpybind-include example.h -- \
     /path/to/example.h -- \
     -D__GENPYBIND__ -xc++ -std=c++14 \
     -I/path/to/some/includes \
     -resource-dir=$HOME/llvm/lib/clang/5.0.0
   ```
   The flags after the second `--` are essentially what you would pass to the compiler when
   processing the translation unit corresponding to the header file.


# License

To be decided.

---

[^1]: During normal compilation these macros have no effect on the generated code, as they are defined
  to be empty.  The annotation system is implemented using the `annotate` attribute specifier, which
  is available as a GNU language extension via `__attribute__((...))`.  As the annotation macros
  only have to be parsed by clang and are empty during normal compilation the annotated code can
  still be compiled by any C++ compiler.  See [genpybind.h](./genpybind.h) for the definition of
  the macros.

[clang]: https://clang.llvm.org/
[pybind11]: https://github.com/pybind/pybind11
[pytest]: https://doc.pytest.org/
