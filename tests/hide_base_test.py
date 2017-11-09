import pytest
import pyhide_base as m

def test_unexposed():
    with pytest.raises(AttributeError) as excinfo:
        m.Unexposed
    assert "has no attribute" in str(excinfo.value)

def test_exposed():
    x = m.Exposed()
    assert x.exposed_base_field == 5

def test_exposed_base():
    x = m.ExposedBase()
    assert x.exposed_base_field == 5
    assert isinstance(x, m.Exposed)

def test_hidden_unexposed_base():
    x = m.HiddenUnexposedBase()
    with pytest.raises(AttributeError) as excinfo:
        x.unexposed_base_field
    assert "has no attribute" in str(excinfo.value)

def test_hidden_exposed_base():
    x = m.HiddenExposedBase()
    with pytest.raises(AttributeError) as excinfo:
        x.exposed_base_field
    assert "has no attribute" in str(excinfo.value)
    assert not isinstance(x, m.Exposed)
