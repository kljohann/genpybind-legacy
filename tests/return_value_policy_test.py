import pyreturn_value_policy as m

def test_default():
    obj = m.Something()
    assert obj.value() == 0

    ref = obj.ref() # returns copy
    assert ref.value == 0
    ref.value = 5
    assert obj.value() == 0 # unchanged

    ref = obj.cref() # returns copy
    assert ref.value == 0
    ref.value = 5
    assert obj.value() == 0 # unchanged

def test_copy():
    obj = m.Something()
    assert obj.value() == 0

    ref = obj.ref_as_copy() # returns copy
    assert ref.value == 0
    ref.value = 5
    assert obj.value() == 0 # unchanged

def test_reference_internal():
    obj = m.Something()
    assert obj.value() == 0

    # returns reference (with keep_alive)
    ref = obj.ref_as_ref_int()
    assert ref.value == 0
    ref.value = 5
    assert obj.value() == 5 # changed!

    ref = obj.cref_as_ref_int()
    assert ref.value == 5
    ref.value = 12
    assert obj.value() == 12 # not changed!
