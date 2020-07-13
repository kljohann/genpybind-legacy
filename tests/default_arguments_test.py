import pytest
import pydefault_arguments as m

@pytest.mark.parametrize("variant", [
    "builtin",
    "class",
    "braced",
    "class_in_namespace",
    "braced_in_namespace",
    "template_in_namespace",
    "class_outside_namespace",
    "braced_outside_namespace",
    "template_outside_namespace",
])
def test_default_arguments(variant):
    # TODO: braced initialization not supported in default argument
    if variant.startswith("braced"):
        pytest.skip("not implemented")
    # TODO: genpybind fails to expand non-type template argument to fully qualified expression
    if variant == "template_in_namespace":
        pytest.skip("not implemented")
    # TODO: genpybind uses `example::Y::N` as default argument?
    if variant == "template_outside_namespace":
        pytest.skip("not implemented")
    fun = getattr(m, "function_{}".format(variant))
    fun()


def test_template_function_with_default():
    assert m.template_function_with_default() == 42
    assert m.template_function_with_default(123) == 123


def test_template_function_with_default_from_function():
    assert m.template_function_with_default_from_function() == 23
    assert m.template_function_with_default_from_function(123) == 123


def test_class_template_member_function_with_default():
    inst = m.HasMemberFunctionWithDefaultArguments_void_()
    assert inst.identity() == 42
    assert inst.identity(123) == 123
