import pytest
import pydynamic_attr as m

def test_default():
    m.Default.what = 5
    obj = m.Default()
    obj.some_function()
    obj.existing_field = False
    with pytest.raises(AttributeError) as excinfo:
        obj.what = 5
    assert "'what' is read-only" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        obj.something = 12
    assert "has no attribute 'something'" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        obj.some_function = 123
    assert "'some_function' is read-only" in str(excinfo.value)

def test_dynamic_attr():
    m.WithDynamic.what = 5
    obj = m.WithDynamic()
    obj.some_function()
    obj.existing_field = False
    obj.something = 12
    assert list(obj.__dict__.keys()) == ["something"]
    assert obj.something == 12
    obj.what = 5
    assert sorted(obj.__dict__.keys()) == ["something", "what"]
    assert obj.what == 5
    obj.some_function = 123
    assert sorted(obj.__dict__.keys()) == ["some_function", "something", "what"]
    assert obj.some_function == 123
