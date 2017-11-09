import pyreturn_value_policy as m

def test_default():
    x = m.Something()
    assert x.value() == 0

    ref = x.ref() # returns copy
    assert ref.value == 0
    ref.value = 5
    assert x.value() == 0 # unchanged

    ref = x.cref() # returns copy
    assert ref.value == 0
    ref.value = 5
    assert x.value() == 0 # unchanged

def test_copy():
    x = m.Something()
    assert x.value() == 0

    ref = x.ref_as_copy() # returns copy
    assert ref.value == 0
    ref.value = 5
    assert x.value() == 0 # unchanged

def test_reference_internal():
    x = m.Something()
    assert x.value() == 0

    # returns reference (with keep_alive)
    ref = x.ref_as_ref_int()
    assert ref.value == 0
    ref.value = 5
    assert x.value() == 5 # changed!

    ref = x.cref_as_ref_int()
    assert ref.value == 5
    ref.value = 12
    assert x.value() == 12 # changed!
