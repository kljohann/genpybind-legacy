#pragma once

#include "genpybind.h"

// Note: This feature will likely be renamed or redesigned, see
// https://github.com/kljohann/genpybind/issues/24.

// TODO: Add tests where the destination of the typename is in a different
// namespace, scope and/or submodule.
// TODO: Add an example where the destination is a templated type

// `opaque(false)` forces the target to be exposed at its own place of
// definition, using its own name.  Any extra keywords specified on the typedef
// will be passed on to the underlying type.  If it has already been made
// visible by an explicit annotation, the extra keywords have no effect and the
// typedef will just be an alias (NOTE: this is likely to change in the future).

struct TargetForOpaqueFalse {};
typedef TargetForOpaqueFalse typedef_opaque_false GENPYBIND(opaque(false));

// Extra arguments to `GENPYBIND` are passed on to underlying type.
struct TargetForOpaqueFalseExtraKeywords {};
typedef TargetForOpaqueFalseExtraKeywords
    typedef_opaque_false_extra_keywords GENPYBIND(opaque(false), dynamic_attr);

// Target already exposed: Extra arguments to `GENPYBIND` have no effect.
struct GENPYBIND(visible) TargetForOpaqueFalseAlreadyExposed {};
typedef TargetForOpaqueFalseAlreadyExposed
    typedef_opaque_false_already_exposed GENPYBIND(opaque(false), dynamic_attr);

// `opaque` or `opaque(true)` forces the target to be exposed at the location
// of the typedef (using the spelling / `expose_as` of the typedef).  If it has
// already been made visible by an explicit annotation or exposed elsewhere an
// error will be emitted during code generation.

// Note: This is the same as `opaque(true)`.
struct TargetForOpaque { int x = 1; };
typedef TargetForOpaque typedef_opaque GENPYBIND(opaque);

struct TargetForOpaqueTrue { int x = 2; };
typedef TargetForOpaqueTrue typedef_opaque_true GENPYBIND(opaque(true));

// Extra arguments to `GENPYBIND` are passed on to underlying type.
struct TargetForOpaqueTrueExtraKeywords {};
typedef TargetForOpaqueTrueExtraKeywords
    typedef_opaque_true_extra_keywords GENPYBIND(opaque(true), dynamic_attr);

// Error: It's not allowed to use `opaque(true)` if the target has already been
// exposed elsewhere.
// struct GENPYBIND(visible) TargetForOpaqueTrueAlreadyExposed {};
// typedef TargetForOpaqueTrueAlreadyExposed
//     typedef_opaque_true_already_exposed GENPYBIND(opaque(true));
