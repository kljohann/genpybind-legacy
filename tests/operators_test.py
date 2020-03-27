import inspect
import operator

import pytest
import pyoperators as m

def test_call_operator():
    obj = m.has_call()
    assert obj(42) == 42
    assert obj(1, 2) == 3

def pythonic_name(name):
    if name in ["and", "or"]:
        name = "{}_".format(name)
    if name == "div":
        name = "truediv"
    if name == "idiv":
        name = "itruediv"
    return name

BINARY_OPERATORS = "lt le eq ne gt ge sub add mul div mod lshift rshift and or xor".split()

@pytest.mark.parametrize("variant", ["member", "friend", "non_const_member"])
@pytest.mark.parametrize("name", BINARY_OPERATORS)
def test_has_binary_operator(variant, name):
    obj = getattr(m, "has_{}_{}".format(variant, name))()
    name = pythonic_name(name)
    assert hasattr(obj, "__{}__".format(name.rstrip("_")))
    assert getattr(operator, name)(obj, obj) is True

@pytest.mark.parametrize("variant", ["hidden", "private", "hidden_friend"])
@pytest.mark.parametrize("name", BINARY_OPERATORS)
def test_has_no_binary_operator(variant, name):
    obj = getattr(m, "has_{}_{}".format(variant, name))()
    if name in ["eq", "ne"]:
        # TODO: sadly, Python 3 seems to synthesize a default function in the
        # absence of __eq__ or __ne__ :(
        return
    name = pythonic_name(name)
    with pytest.raises(TypeError, match="|".join([
            r"not supported between instances of",
            r"unsupported operand type\(s\)",
    ])):
        getattr(operator, name)(obj, obj)

UNARY_OPERATORS = "iadd isub imul idiv imod ilshift irshift iand ior ixor".split()

@pytest.mark.parametrize("name", UNARY_OPERATORS)
def test_has_unary_operator(name):
    obj = m.has_unary()
    pyname = pythonic_name(name)
    assert hasattr(obj, "__{}__".format(pyname))
    obj = getattr(operator, pyname)(obj, 42)
    for key, val in inspect.getmembers(obj):
        if key == name:
            assert val == 42
        elif key in UNARY_OPERATORS:
            assert val == 0

NULLARY_OPERATORS = "neg pos invert".split()

@pytest.mark.parametrize("name", NULLARY_OPERATORS)
def test_has_nullary_operator(name):
    obj = m.has_nullary()
    pyname = pythonic_name(name)
    assert hasattr(obj, "__{}__".format(pyname))
    obj = getattr(operator, pyname)(obj)
    for key, val in inspect.getmembers(obj):
        if key == name:
            assert val is True
        elif key in NULLARY_OPERATORS:
            assert val is False

@pytest.mark.skip(reason="not implemented")
def test_has_floordiv():
    obj = m.has_floordiv()
    assert not hasattr(obj, "__truediv__")
    assert hasattr(obj, "__floordiv__")
    assert obj // 5 == 8

@pytest.mark.skip(reason="not implemented")
def test_has_friend_floordiv():
    obj = m.has_friend_floordiv()
    assert not hasattr(obj, "__truediv__")
    assert hasattr(obj, "__floordiv__")
    assert isinstance(obj // obj, m.has_friend_floordiv)
