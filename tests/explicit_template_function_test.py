import pytest
import pyexplicit_template_function as m

def test_free_function_int():
    val = m.frobnicate(5)
    assert val == 37
    try:
        assert isinstance(val, (int, long))
    except NameError: # Python 3 does not have 'long'
        assert isinstance(val, int)

def test_free_function_float():
    val = m.frobnicate(5.0)
    assert val == 37.0
    assert isinstance(val, float)

def test_free_function_invalid():
    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.frobnicate("uiae")

def test_member_function_int():
    obj = m.Klass()
    assert obj.increase(5) == 6

def test_member_function_invalid():
    obj = m.Klass()
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.increase("uiae")

def test_constructor():
    obj = m.Something()
    assert obj.value == 0
    obj = m.Something(123)
    assert obj.value == 123
