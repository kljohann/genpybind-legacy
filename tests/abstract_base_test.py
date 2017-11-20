import pytest
import pyabstract_base as m

def test_base():
    with pytest.raises(TypeError) as excinfo:
        m.AbstractBase()
    assert "No constructor defined!" in str(excinfo.value)
    assert m.AbstractBase.static_method() is True

def test_derived():
    obj = m.Derived()
    assert m.Derived.static_method() is True
    assert obj.whatever(42) == 42
    assert obj.something(42) == -42
    assert obj.return_magic_number() == 42.0
