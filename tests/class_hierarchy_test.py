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
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.overloaded(5, 7)
    assert obj.base_field == 0
    obj.base_field = 42
    assert obj.base_field == 42

def test_derived_private():
    obj = m.DerivedPrivate()
    assert isinstance(obj, m.DerivedPrivate)
    assert not isinstance(obj, m.Base)
    assert not hasattr(obj, "from_base")
    assert obj.overloaded(5) is False
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.overloaded(5, 7)
    assert not hasattr(obj, "base_field")

def test_derived_inline():
    obj = m.DerivedInline()
    assert isinstance(obj, m.DerivedInline)
    assert not isinstance(obj, m.Base)
    assert obj.from_base() is True
    assert obj.overloaded(5) is False
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.overloaded(5, 7)
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
