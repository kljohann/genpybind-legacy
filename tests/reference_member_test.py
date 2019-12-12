import pytest
import pyreference_member as m

def test_reference_member():
    x = m.Nested(value=3)

    obj = m.ReferenceMember(x)
    assert obj.nested.value == 3

    # set obj.nested.value via x
    x.value = 10
    assert obj.nested.value == 10

    # set x.value via obj.nested
    obj.nested.value = 11
    assert x.value == 11


def test_cannot_be_set_to_wrong_type():
    x = m.Nested(value=3)

    obj = m.ReferenceMember(x)
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.nested = 123


def test_identity_of_reference_member():
    """Test that the setter modifies the instance used during construction.

    In the following, setting the property leads to a call of the implicit
    copy assignment operator on the instance `x`.
    As a consequence `obj.nested` will always point to `x`.
    """
    x = m.Nested(value=123)
    y = m.Nested(value=124)
    assert y is not x

    obj = m.ReferenceMember(x)
    assert obj.nested is x
    assert obj.nested is not y

    obj.nested = y
    assert obj.nested.value == 124
    assert x.value == 124
    assert obj.nested is x
    assert obj.nested is not y
