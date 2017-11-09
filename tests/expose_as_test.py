import pytest
import pyexpose_as as m

def test_enum():
    with pytest.raises(AttributeError):
        m.some_enum
    assert m.enum.A != m.enum.B

def test_free_function():
    with pytest.raises(AttributeError):
        m.free_function
    m.free_function_()

def test_static_variable():
    with pytest.raises(AttributeError):
        m.x
    assert m.x_instance.xfield == 15

def test_conversion_operator():
    d = m.Dummy(5)
    assert d.__int__() == 5
    assert int(d) == 5

def test_member_function():
    d = m.Dummy(42)
    with pytest.raises(AttributeError):
        d.hash
    assert d.__hash__() == 42
    assert hash(d) == 42

def test_member_variable():
    d = m.Dummy(12)
    with pytest.raises(AttributeError):
        d.member
    assert d.member_ == True

def test_static_member_variable():
    with pytest.raises(AttributeError):
        m.Dummy.constant
    assert m.Dummy.constant_ == True

def test_static_member_function():
    with pytest.raises(AttributeError):
        m.Dummy.function
    assert m.Dummy.static() == True

def test_typedef():
    with pytest.raises(AttributeError):
        m.Dummy.type
    assert m.Dummy.typedef == m.X

def test_opaque_typedef():
    with pytest.raises(AttributeError):
        m.Dummy.y_type
    assert m.Dummy.y_type_().yfield == 42
