import pytest
from genpybind.annotations import Annotations

def as_list(inp):
    return list(Annotations(inp))

def test_example():
    inp = "plain, call(), with_arg(some_name), with_args(a, b, c, 1, 2, 3, 'hello', \"world\")"
    assert as_list(inp) == [
        ("plain", ()),
        ("call", ()),
        ("with_arg", ("some_name",)),
        ("with_args", ("a", "b", "c", 1, 2, 3, "hello", "world")),
    ]

def test_plain():
    assert as_list("plain") == [("plain", ())]

def test_multiple():
    assert as_list(["multiple", "attributes(are, supported)"]) == [
        ("multiple", ()),
        ("attributes", ("are", "supported"))
    ]

def test_special_names():
    assert as_list("required(true), visible(false), whatever(default), none(none)") == [
        ("required", (True,)),
        ("visible", (False,)),
        ("whatever", (None,)),
        ("none", (None,)),
    ]

@pytest.mark.parametrize("spelling", ["true", "True"])
def test_special_true(spelling):
    assert as_list("value({})".format(spelling)) == [("value", (True,))]

@pytest.mark.parametrize("spelling", ["false", "False"])
def test_special_false(spelling):
    assert as_list("value({})".format(spelling)) == [("value", (False,))]

@pytest.mark.parametrize("spelling", ["none", "None", "default", "Default"])
def test_special_none(spelling):
    assert as_list("value({})".format(spelling)) == [("value", (None,))]
