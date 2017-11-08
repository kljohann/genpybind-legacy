import pytest
import pyexplicit_template_function as m

def test_free_function_int():
    v = m.frobnicate(5)
    assert v == 37
    assert type(v) in [int, long]

def test_free_function_float():
    v = m.frobnicate(5.0)
    assert v == 37.0
    assert type(v) == float

def test_free_function_invalid():
    with pytest.raises(TypeError) as excinfo:
        m.frobnicate("uiae")

    assert("incompatible function arguments" in str(excinfo.value))

def test_member_function_int():
    k = m.Klass()
    assert k.increase(5) == 6

def test_member_function_invalid():
    k = m.Klass()
    with pytest.raises(TypeError) as excinfo:
        k.increase("uiae")

    assert("incompatible function arguments" in str(excinfo.value))
