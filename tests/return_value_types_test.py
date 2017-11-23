import pytest
import pyreturn_value_types as m

@pytest.mark.parametrize("variant", [
    "builtin",
    "class",
    "class_in_namespace",
    "template_in_namespace",
    "class_outside_namespace",
    "template_outside_namespace",
])
def test_default_arguments(variant):
    # TODO: genpybind fails to expand non-type template argument to fully qualified expression
    if variant == "template_in_namespace":
        pytest.skip("not implemented")
    fun = getattr(m, "return_{}".format(variant))
    fun()
