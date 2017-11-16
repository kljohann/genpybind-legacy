import pytest
import pyannotations as m

def test_visible():
    _obj = m.Plain()
    _obj = m.AsCall()
    obj = m.WithArgTrue()
    obj.with_arg_default # pylint: disable=pointless-statement
    with pytest.raises(AttributeError) as excinfo:
        obj.with_arg_false # pylint: disable=pointless-statement
    assert "has no attribute 'with_arg_false'" in str(excinfo.value)

@pytest.mark.parametrize("args", [(1, 1., 1.), (1., 1, 1.), (1., 1., 1)])
def test_noconvert(args):
    with pytest.raises(TypeError) as excinfo:
        m.multiple_mixed_args(*args)
    assert "incompatible function arguments" in str(excinfo.value)
