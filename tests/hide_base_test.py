import pytest
import pyhide_base as m

def test_unexposed():
    with pytest.raises(AttributeError) as excinfo:
        m.Unexposed # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

def test_exposed():
    obj = m.Exposed()
    assert obj.exposed_base_field == 5

def test_exposed_base():
    obj = m.ExposedBase()
    assert obj.exposed_base_field == 5
    assert isinstance(obj, m.Exposed)

def test_hidden_unexposed_base():
    obj = m.HiddenUnexposedBase()
    with pytest.raises(AttributeError) as excinfo:
        obj.unexposed_base_field # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)

def test_hidden_exposed_base():
    obj = m.HiddenExposedBase()
    with pytest.raises(AttributeError) as excinfo:
        obj.exposed_base_field # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
    assert not isinstance(obj, m.Exposed)
