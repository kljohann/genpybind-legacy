import pytest
import pyproperties as m

def test_property():
    obj = m.Something()
    assert obj.value == 0
    assert not hasattr(obj, "get_value")

    obj.value = 5
    assert not hasattr(obj, "set_value")
    assert obj.value == 5

def test_other_property():
    obj = m.Something()
    assert obj.other == 0
    assert not hasattr(obj, "get_other")

    obj.other = 5
    assert not hasattr(obj, "set_other")
    assert obj.other == 5

def test_readonly_property():
    obj = m.Something()
    assert obj.readonly is True
    assert not hasattr(obj, "computed")

    with pytest.raises(AttributeError, match="can't set attribute"):
        obj.readonly = 5
