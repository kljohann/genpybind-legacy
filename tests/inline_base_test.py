import pytest
import pyinline_base as m

def test_inline_base():
    obj = m.Derived()
    assert isinstance(obj, m.Derived)
    assert obj.member_function() == 42
    classes = [c.__name__ for c in m.Derived.mro()]
    assert "Derived" in classes
    assert not "Base" in classes

def test_derived_multiple():
    obj = m.DerivedMultiple()
    assert isinstance(obj, m.DerivedMultiple)
    assert isinstance(obj, m.OtherBase)
    assert obj.member_function() == 42
    assert obj.from_other_base() is True
    classes = [c.__name__ for c in m.DerivedMultiple.mro()]
    assert "DerivedMultiple" in classes
    assert not "Base" in classes
    assert "OtherBase" in classes

def test_derived_derived():
    obj = m.DerivedDerived()
    assert isinstance(obj, m.DerivedDerived)
    assert obj.member_function() == 42
    classes = [c.__name__ for c in m.DerivedDerived.mro()]
    assert "DerivedDerived" in classes
    assert "Derived" in classes
    assert not "Base" in classes

def test_derived_derived_multiple():
    obj = m.DerivedDerivedMultiple()
    assert isinstance(obj, m.DerivedDerivedMultiple)
    assert isinstance(obj, m.OtherBase)
    assert obj.member_function() == 42
    assert obj.from_other_base() is True
    classes = [c.__name__ for c in m.DerivedDerivedMultiple.mro()]
    assert "DerivedDerivedMultiple" in classes
    assert "Derived" in classes
    assert not "Base" in classes
    assert "OtherBase" in classes

def test_derived_indirect():
    obj = m.DerivedIndirect()
    assert isinstance(obj, m.DerivedIndirect)
    assert obj.member_function() == 42
    assert obj.from_indirect() is True
    classes = [c.__name__ for c in m.DerivedIndirect.mro()]
    assert "DerivedIndirect" in classes
    assert not "Base" in classes
    assert not "Indirect" in classes

def test_derived_indirect_hide():
    obj = m.DerivedHide()
    assert isinstance(obj, m.DerivedHide)
    with pytest.raises(AttributeError) as excinfo:
        obj.member_function # pylint: disable=pointless-statement
    assert "" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        obj.from_indirect # pylint: disable=pointless-statement
    assert "" in str(excinfo.value)
    classes = [c.__name__ for c in m.DerivedHide.mro()]
    assert "DerivedHide" in classes
    assert not "Base" in classes
    assert not "Indirect" in classes
