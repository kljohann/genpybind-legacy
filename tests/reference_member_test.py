import pytest
import pyreference_member as m

def test_reference_member():
    referred_to = m.Nested(value=3)

    obj = m.ReferenceMember(referred_to)
    assert obj.nested.value == 3

    # set obj.nested.value via referred_to
    referred_to.value = 10
    assert obj.nested.value == 10

    # set referred_to.value via obj.nested
    obj.nested.value = 11
    assert referred_to.value == 11


def test_cannot_be_set_to_wrong_type():
    referred_to = m.Nested(value=3)

    obj = m.ReferenceMember(referred_to)
    with pytest.raises(TypeError, match="incompatible function arguments"):
        obj.nested = 123


def test_identity_of_reference_member():
    """Test that the setter modifies the instance used during construction.

    In the following, setting the property leads to a call of the implicit
    copy assignment operator on the instance `referred_to`.
    As a consequence `obj.nested` will always point to `referred_to`.
    """
    referred_to = m.Nested(value=123)
    copied_from = m.Nested(value=124)
    assert copied_from is not referred_to

    obj = m.ReferenceMember(referred_to)
    assert obj.nested is referred_to
    assert obj.nested is not copied_from

    obj.nested = copied_from
    assert obj.nested.value == 124
    assert referred_to.value == 124
    assert obj.nested is referred_to
    assert obj.nested is not copied_from
