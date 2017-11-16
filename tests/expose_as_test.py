import pytest
import pyexpose_as as m

def test_enum():
    with pytest.raises(AttributeError):
        m.some_enum # pylint: disable=pointless-statement
    assert m.enum.A != m.enum.B

def test_free_function():
    with pytest.raises(AttributeError):
        m.free_function # pylint: disable=pointless-statement
    m.free_function_()

def test_static_variable():
    with pytest.raises(AttributeError):
        m.x # pylint: disable=pointless-statement
    assert m.x_instance.xfield == 15

def test_conversion_operator():
    obj = m.Dummy(5)
    assert obj.__int__() == 5
    assert int(obj) == 5

def test_member_function():
    obj = m.Dummy(42)
    with pytest.raises(AttributeError):
        obj.hash # pylint: disable=pointless-statement
    assert obj.__hash__() == 42
    assert hash(obj) == 42

def test_member_variable():
    obj = m.Dummy(12)
    with pytest.raises(AttributeError):
        obj.member # pylint: disable=pointless-statement
    assert obj.member_ is True

def test_static_member_variable():
    with pytest.raises(AttributeError):
        m.Dummy.constant # pylint: disable=pointless-statement
    assert m.Dummy.constant_ is True

def test_static_member_function():
    with pytest.raises(AttributeError):
        m.Dummy.function # pylint: disable=pointless-statement
    assert m.Dummy.static() is True

def test_typedef():
    with pytest.raises(AttributeError):
        m.Dummy.type # pylint: disable=pointless-statement
    assert m.Dummy.typedef == m.X

def test_opaque_typedef():
    with pytest.raises(AttributeError):
        m.Dummy.y_type # pylint: disable=pointless-statement
    assert m.Dummy.y_type_().yfield == 42
