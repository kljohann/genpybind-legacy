import pyvariant_parameters as m

def test_variant_parameters():
    assert hasattr(m, 'foo')
    assert m.foo(3) == 3
    assert m.foo("s") == "s"
