# genpybind [![CircleCI](https://circleci.com/gh/kljohann/genpybind.svg?style=svg)](https://circleci.com/gh/kljohann/genpybind)

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

- Documentation is minimal at the moment.  If you want to look at example use-cases the
  [integration tests](./tests) might provide a starting point.
- Expressions and types in default arguments, return values or `GENPYBIND_MANUAL` instructions are
  not consistently expanded to their fully qualified form.  As a workaround it is suggested to use
  the fully-qualified name where necessary.

# Installation

_Note: genpybind requires Python version 3.7 or above._

1. Build and install llvm/clang 9.0.0 with the patches provided in `llvm-patches`.  You can use a
   different prefix when installing, to prevent the patched clang from interfering with the version
   provided by your distribution.  Let's assume you unpacked the source code to `$HOME/llvm-src` and
   used `-DCMAKE_INSTALL_PREFIX=$HOME/llvm`.
2. Make sure genpybind can find the the libclang Python bindings:
   ```bash
   export PYTHONPATH=$HOME/llvm-src/tools/clang/bindings/python \
     LD_LIBRARY_PATH=$HOME/llvm/lib
   ```
3. Build the `genpybind-parse` executable:
   ```bash
   PYTHON=/usr/bin/python3 CXX=/bin/clang++ CC=/bin/clang \
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
     -resource-dir=$HOME/llvm/lib/clang/9.0.0
   ```
   The flags after the second `--` are essentially what you would pass to the compiler when
   processing the translation unit corresponding to the header file.

# Keywords

## `arithmetic`

```cpp
enum GENPYBIND(arithmetic) Access { Read = 4, Write = 2, Execute = 1 };
```

To allow arithmetic on `enum` elements use the `arithmetic` keyword.

See [enums.h](./tests/enums.h) and [enums_test.py](./tests/enums_test.py).

## `dynamic_attr`

The `dynamic_attr` keyword controls if dynamic attributes (adding additional members at run-time) is allowed:

```cpp
struct GENPYBIND(visible) Default {
  void some_function() const {}
  bool existing_field = true;
};

struct GENPYBIND(dynamic_attr) WithDynamic {
  void some_function() const {}
  bool existing_field = true;
};
```

See [dynamic_attr.h](./tests/dynamic_attr.h) and [dynamic_attr_test.py](./tests/dynamic_attr_test.py).

## `expose_as`

`expose_as` allows to give the Python binding a name different from the one in the C++ source:

```cpp
GENPYBIND(expose_as(some_other_name));
bool name;
```

This also allows to populate the private/name-mangled Python variables and functions:

```cpp
GENPYBIND(expose_as(__hash__))
int hash() const;
```

See [expose_as.h](./tests/expose_as.h) and [expose_as_test.py](./tests/expose_as_test.py).

## `getter_for`/`setter_for`/`accessor_for`

Python propiertes are supported by the `getter_for` and `setter_for` keywords:

```cpp
GENPYBIND(getter_for(value))
int get_value() const;

GENPYBIND(setter_for(value))
void set_value(int value);

GENPYBIND(getter_for(readonly))
bool computed() const;
```

`getter` and `setter_for` are short-hands for `accessor_for(..., get/set)`.

See [properties.h](./tests/properties.h) and [properties_test.py](./tests/properties_test.py).

## `hidden`

See [visible](#visible).

## `hide_base`

See [hide_base.h](./tests/hide_base.h) and [hide_base_test.py](./tests/hide_base_test.py).

## `holder_type`

Cf. [pybind11's][pybind11] `PYBIND11_DECLARE_HOLDER_TYPE`.

See [holder_type.h](./tests/holder_type.h) and [holder_type_test.py](./tests/holder_type_test.py).

## `inline_base`

See [inline_base.h](./tests/inline_base.h) and [inline_base_test.py](./tests/inline_base_test.py).

## `keep_alive`

To control the life time of objects passed to or returned from (member) functions, `keep_alive` can be used.
`keep_alive(bound, who)` indicates that `who` should be kept alive at least until `bound` is garbage collected.
An argument to `keep_alive` can be either the name of a function parameters or one of `return` or `this`, where
`return` refers to the return value of the function and `this` refers to the instance a member function is called on.

```cpp
GENPYBIND(keep_alive(this, child))
Parent(Child *child);
```

When the instance of `Parent` is deleted from Python, `child` will not be deleted as well.

See [keep_alive.h](./tests/keep_alive.h) and [keep_alive_test.py](./tests/keep_alive_test.py).

## `module`

Using the `module` keyword C++ namespaces can be turned into submodules
of the generated Python module. In the following example, `X` would be exposed
as `name_of_module.submodule.X`, where `name_of_module` is the name of the
outer Python module.

```cpp
namespace submodule GENPYBIND(module) {
class GENPYBIND(visible) X {};
} // namespace submodule
```

See [submodule.h](./tests/submodule.h) and [submodule_test.py](./tests/submodule_test.py).

## `noconvert`

Implicit conversion of function arguments can be controlled with the `noconvert` keyword:

```cpp
GENPYBIND(noconvert(value))
double noconvert(double value);

GENPYBIND(noconvert(first))
double noconvert_first(double first, double second);
```

If `noconvert(...)` is called with anything but type `double`, a `TypeError` is raised.
For multi-argument functions, the behaviour can be controlled on a per-variable basis.

See [noconvert.h](./tests/noconvert.h) and [noconvert_test.py](./tests/noconvert_test.py).

## `opaque`

Allows to "inline" the underlying type at the location of a typedef, as if it was defined
there.  As the name of this feature may lead to confusion with [pybind11's][pybind11]
`PYBIND11_MAKE_OPAQUE`, it will likely be renamed or redesigned in an upcoming release.
More details can be found in [issue #24](https://github.com/kljohann/genpybind/issues/24).

See [expose_as.h](./tests/expose_as.h) and [expose_as_test.py](./tests/expose_as_test.py).

## `postamble`

Unscoped `GENPYBIND_MANUAL` macros can be used to add preamble and postamble code to the
generated bindings, e.g. for importing required libraries or executing python code that
dynamically patches the generated bindings:

```cpp
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
```

See [manual.h](./tests/manual.h) and [manual_test.py](./tests/manual_test.py).

## `readonly`

`readonly` is an alias for `writable(false)`;

## `required`

```cpp
GENPYBIND(required(child))
void required(Child *child)
```

Calls to functions where pointer arguments are annotated with `required`
and called from Python with `None` will raise a `TypeError`.

See [required.h](./tests/required.h) and [required_test.py](./tests/required_test.py).

## `return_value_policy`

The return value policy controls how returned references are exposed to Python:

```cpp
Nested &ref();

const Nested &cref() const;

GENPYBIND(return_value_policy(copy))
Nested &ref_as_copy();

struct GENPYBIND(visible) Parent {
  GENPYBIND(return_value_policy(reference_internal))
  Nested &ref_as_ref_int();
};
```

By default, the `automatic` [return value policy](https://pybind11.readthedocs.io/en/master/advanced/functions.html#return-value-policies)
of pybind11 is used.  In the case of `ref` and `cref` in the example this amounts to
"return by value" for the wrapped Python functions. This behavior is unchanged
when the function is explicitly annotated to return by value (see `ref_as_copy`).
As `ref_as_ref_int` demonstrates, any other return value policy supported by
pybind11 can be set. In this case `reference_internal` is used to return a reference
to an existing object, whose life time  is tied to the parent object.

See [return_by_value_policy.h](./tests/return_by_value_policy.h) and [return_by_value_policy_test.py](./tests/return_by_value_policy_test.py).

## `stringstream`

The `stringstream` keyword populates the `str` and `repr` functionality:

```cpp
GENPYBIND(stringstream)
friend std::ostream &operator<<(std::ostream &os, const Something &) {
  return os << "uiae";
}
```

See [stringstream.h](./tests/stringstream.h) and [stringstream_test.py](./tests/stringstream_test.py).

## `visible`

If a binding is supposed to be generated is controlled by the visibility keywords `visible` and `hidden`:

```cpp
class Unannotated {};

class GENPYBIND(hidden) Hidden {};

class GENPYBIND(visible) Visible {};
```

Any `GENPYBIND` annotation will make the annotated entity visible.
As a consequence `visible` can be removed from the argument list,
as soon as there are any other arguments to `GENPYBIND`.

Anything without an annotation is excluded by default, but the intent of hiding it
from bindings can be explicitly stated by the keyword `hidden`.

If a namespace is annotated with `visible`, any contained entity will be made visible
by default, even if it has no `GENPYBIND` annotations.  The `hidden` keyword can then
be used to hide it.

See [visibility.h](./tests/visibility.h) and [visibility_test.py](./tests/visibility_test.py).

## `writeable`

Constness is transported from C++ to Python automatically. In addition, variables can be set to be read-only by the `writable` keyword:

```cpp
const int const_field = 2;
GENPYBIND(writeable(false))
int readonly_field = 4;
```

For both `const_field` and `readonly_field`, an `AttributeError` will be raised if set from Python.

See [variables.h](./tests/variables.h) and [variables_test.py](./tests/variables_test.py).

# License

See [License](LICENSE).

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
