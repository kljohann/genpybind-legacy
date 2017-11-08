#pragma once

#include "genpybind.h"

class Unannotated {};

class GENPYBIND(hidden) Hidden {};

class GENPYBIND(visible) Visible {
public:
  static constexpr bool public_constant = true;
  static constexpr bool GENPYBIND(hidden) hidden_public_constant = false;

protected:
  static constexpr bool protected_constant = false;

private:
  static constexpr bool private_constant = false;
};

namespace default_visibility {
class UnannotatedInNamespace {}; // should be hidden
} // namespace default_visibility

namespace visible_namespace GENPYBIND(visible) {
class UnannotatedInVisibleNamespace {}; // should be visible
class GENPYBIND(visible) VisibleInVisibleNamespace {}; // should be visible
class GENPYBIND(visible(false)) VisibleFalseInVisibleNamespace {}; // should be hidden
class GENPYBIND(visible(default)) VisibleDefaultInVisibleNamespace {}; // should be visible
class GENPYBIND(hidden) HiddenInVisibleNamespace {}; // should be hidden

namespace default_namespace {
class UnannotatedInNamespaceInVisibleNamespace {}; // should be visible
} // namespace default_namespace

namespace hidden_namespace GENPYBIND(hidden) {
class UnannotatedInHiddenNamespaceInVisibleNamespace {}; // should be hidden
} // namespace hidden_namespaceGENPYBIND(hidden)
} // namespace visible_namespaceGENPYBIND(visible)

// The following (convoluted) example is for a class that will not be exposed at
// its original location but used elsewhere using an "opaque" typedef to mark
// the desired location. Note that we have to explicitly specify the visibility
// because it would otherwise be inferred to `visible` due to other annotations
// being present.  To hide this class we could just use the `hidden` attribute,
// but as visibility is inherited by children they would be marked as hidden as
// well.  As this would lead to the member field being hidden in the new
// location, we instead use `visible(default)` to use the default visibility
// based on context.
struct GENPYBIND(visible(default), dynamic_attr) UsedIndirectly {
  static constexpr bool should_be_visible = true;
  static constexpr bool GENPYBIND(hidden) should_be_hidden = true;
};

struct GENPYBIND(visible) SomeScope {
  typedef UsedIndirectly ExposedHere GENPYBIND(opaque);
};
