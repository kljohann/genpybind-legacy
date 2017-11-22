import pyoverloads as m

def test_constructors():
    assert m.Something().value == 0
    assert m.Something(42).value == 42
    assert m.Something(1, 2).value == 3

def test_member_functions():
    obj = m.Something(42)
    assert obj.value == 42
    obj.set()
    assert obj.value == 0
    obj.set(42)
    assert obj.value == 42
    obj.set(1, 2)
    assert obj.value == 3

def test_free_functions():
    assert m.overloaded(42) == 42
    assert m.overloaded(1, 2) == 3
