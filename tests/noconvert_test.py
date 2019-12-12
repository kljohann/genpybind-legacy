import pytest
import pynoconvert as m

def test_overloading():
    assert m.called_with_double(5.0) is True
    assert m.called_with_double(5) is False

def test_conversion():
    assert m.convert(5.0) == 5.0
    assert m.convert(5) == 5.0

def test_noconvert():
    assert m.noconvert(5.0) == 5.0
    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.noconvert(5)

def test_noconvert_first():
    assert m.noconvert_first(5.0, 7.0) == 12.0
    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.noconvert_first(5, 7.0)
    assert m.noconvert_first(5.0, 7) == 12.0

def test_noconvert_numeric():
    assert m.noconvert_numeric(5.0, 7.0) == 12.0
    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.noconvert_numeric(5, 7.0)
    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.noconvert_numeric(5.0, 7)
