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
