import pytest
import pyproperties as m

def test_property():
    obj = m.Something()
    assert obj.value == 0

    with pytest.raises(AttributeError) as excinfo:
        obj.get_value # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

    obj.value = 5

    with pytest.raises(AttributeError) as excinfo:
        obj.set_value # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

    assert obj.value == 5

def test_other_property():
    obj = m.Something()
    assert obj.other == 0

    with pytest.raises(AttributeError) as excinfo:
        obj.get_other # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

    obj.other = 5

    with pytest.raises(AttributeError) as excinfo:
        obj.set_other # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

    assert obj.other == 5

def test_readonly_property():
    obj = m.Something()
    assert obj.readonly is True

    with pytest.raises(AttributeError) as excinfo:
        obj.computed # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        obj.readonly = 5
    assert "can't set attribute" in str(excinfo.value)

def test_property_based_on_overloaded_functions():
    obj = m.Something()
    assert not hasattr(obj, "get_overloaded")
    assert not hasattr(obj, "set_overloaded")

    assert obj.overloaded == 0
    obj.overloaded = 123
    assert obj.overloaded == 123

    arg = m.Argument()
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.overloaded = arg
