import pyinline_base as m

def test_inline_base():
    obj = m.Derived()
    assert isinstance(obj, m.Derived)
    assert obj.member_function() == 42
    classes = [c.__name__ for c in m.Derived.mro()]
    assert "Derived" in classes
    assert not "Base" in classes
    # assert m.Derived.__mro__
