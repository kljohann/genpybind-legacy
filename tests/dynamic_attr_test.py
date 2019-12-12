import pytest
import pydynamic_attr as m

def test_default():
    m.Default.what = 5
    obj = m.Default()
    obj.some_function()
    obj.existing_field = False
    with pytest.raises(AttributeError, match="'what' is read-only"):
        obj.what = 5
    assert not hasattr(obj, "something")
    with pytest.raises(AttributeError, match="'some_function' is read-only"):
        obj.some_function = 123

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
