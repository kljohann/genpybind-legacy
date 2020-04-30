import pyhide_base as m

def test_unexposed():
    assert not hasattr(m, "Unexposed")

def test_exposed():
    obj = m.Exposed()
    assert obj.exposed_base_field == 5

def test_exposed_base():
    obj = m.ExposedBase()
    assert obj.exposed_base_field == 5
    assert isinstance(obj, m.Exposed)

def test_hidden_unexposed_base():
    obj = m.HiddenUnexposedBase()
    assert not hasattr(obj, "unexposed_base_field")

def test_hidden_exposed_base():
    obj = m.HiddenExposedBase()
    assert not hasattr(obj, "exposed_base_field")
    assert not isinstance(obj, m.Exposed)
