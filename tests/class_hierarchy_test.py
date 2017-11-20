import pytest
import pyclass_hierarchy as m

def test_base():
    obj = m.Base()
    assert obj.from_base() is True
    assert obj.overloaded(5) is True
    assert obj.overloaded(5, 7) is True
    assert obj.base_field == 0
    obj.base_field = 42
    assert obj.base_field == 42

def test_derived_public():
    obj = m.DerivedPublic()
    assert isinstance(obj, m.DerivedPublic)
    assert isinstance(obj, m.Base)
    assert obj.from_base() is True
    assert obj.overloaded(5) is False
    with pytest.raises(TypeError) as excinfo:
        obj.overloaded(5, 7)
    assert "incompatible function arguments" in str(excinfo.value)
    assert obj.base_field == 0
    obj.base_field = 42
    assert obj.base_field == 42

def test_derived_private():
    obj = m.DerivedPrivate()
    assert isinstance(obj, m.DerivedPrivate)
    assert not isinstance(obj, m.Base)
    with pytest.raises(AttributeError) as excinfo:
        obj.from_base()
    assert "has no attribute 'from_base'" in str(excinfo.value)
    assert obj.overloaded(5) is False
    with pytest.raises(TypeError) as excinfo:
        obj.overloaded(5, 7)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        obj.base_field # pylint: disable=pointless-statement
    assert "has no attribute 'base_field'" in str(excinfo.value)

@pytest.mark.skip(reason="not working")
def test_derived_inline():
    obj = m.DerivedInline()
    assert isinstance(obj, m.DerivedInline)
    assert not isinstance(obj, m.Base)
    assert obj.from_base() is True
    assert obj.overloaded(5) is False
    with pytest.raises(TypeError) as excinfo:
        obj.overloaded(5, 7)
    assert "incompatible function arguments" in str(excinfo.value)
    assert obj.base_field == 0
    obj.base_field = 42
    assert obj.base_field == 42

def test_derived_multiple():
    obj = m.DerivedMultiple()
    assert isinstance(obj, m.DerivedMultiple)
    assert isinstance(obj, m.Base)
    assert isinstance(obj, m.OtherBase)
    assert obj.base_field == 0
    obj.base_field = 42
    assert obj.base_field == 42
