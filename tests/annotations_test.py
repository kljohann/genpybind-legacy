import pytest
import pyannotations as m

def test_visible():
    _obj = m.Plain()
    _obj = m.AsCall()
    obj = m.WithArgTrue()
    assert hasattr(obj, "with_arg_default")
    assert not hasattr(obj, "with_arg_false")

@pytest.mark.parametrize("args", [(1, 1., 1.), (1., 1, 1.), (1., 1., 1)])
def test_noconvert(args):
    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.multiple_mixed_args(*args)
