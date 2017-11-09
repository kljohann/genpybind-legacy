import pytest
import pyproperties as m

def test_property():
    x = m.Something()
    assert x.value == 0

    with pytest.raises(AttributeError) as excinfo:
        x.get_value
    assert "has no attribute" in str(excinfo.value)

    x.value = 5

    with pytest.raises(AttributeError) as excinfo:
        x.set_value
    assert "has no attribute" in str(excinfo.value)

    assert x.value == 5

def test_other_property():
    x = m.Something()
    assert x.other == 0

    with pytest.raises(AttributeError) as excinfo:
        x.get_other
    assert "has no attribute" in str(excinfo.value)

    x.other = 5

    with pytest.raises(AttributeError) as excinfo:
        x.set_other
    assert "has no attribute" in str(excinfo.value)

    assert x.other == 5

def test_readonly_property():
    x = m.Something()
    assert x.readonly == True

    with pytest.raises(AttributeError) as excinfo:
        x.computed
    assert "has no attribute" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        x.readonly = 5
    assert "can't set attribute" in str(excinfo.value)
