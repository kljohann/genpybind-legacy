import pyexpose_as as m

def test_enum():
    assert not hasattr(m, "some_enum")
    assert m.enum.A != m.enum.B

def test_free_function():
    assert not hasattr(m, "free_function")
    m.free_function_()

def test_static_variable():
    assert not hasattr(m, "x")
    assert m.x_instance.xfield == 15

def test_conversion_operator():
    obj = m.Dummy(5)
    assert obj.__int__() == 5
    assert int(obj) == 5

def test_member_function():
    obj = m.Dummy(42)
    assert not hasattr(obj, "hash")
    assert obj.__hash__() == 42
    assert hash(obj) == 42

def test_member_variable():
    obj = m.Dummy(12)
    assert not hasattr(obj, "member")
    assert obj.member_ is True

def test_static_member_variable():
    assert not hasattr(m.Dummy, "constant")
    assert m.Dummy.constant_ is True

def test_static_member_function():
    assert not hasattr(m.Dummy, "function")
    assert m.Dummy.static() is True

def test_typedef():
    assert not hasattr(m.Dummy, "type")
    assert m.Dummy.typedef == m.X

def test_opaque_typedef():
    assert not hasattr(m.Dummy, "y_type")
    assert m.Dummy.y_type_().yfield == 42
