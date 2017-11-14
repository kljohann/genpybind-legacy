import pytest
import pydynamic_attr as m

def test_default():
    m.Default.what = 5
    x = m.Default()
    x.some_function()
    x.existing_field = False
    with pytest.raises(AttributeError) as excinfo:
        x.what = 5
    assert "'what' is read-only" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        x.something = 12
    assert "has no attribute 'something'" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        x.some_function = 123
    assert "'some_function' is read-only" in str(excinfo.value)

def test_dynamic_attr():
    m.WithDynamic.what = 5
    x = m.WithDynamic()
    x.some_function()
    x.existing_field = False
    x.something = 12
    assert list(x.__dict__.keys()) == ["something"]
    assert x.something == 12
    x.what = 5
    assert sorted(x.__dict__.keys()) == ["something", "what"]
    assert x.what == 5
    x.some_function = 123
    assert sorted(x.__dict__.keys()) == ["some_function", "something", "what"]
    assert x.some_function == 123
