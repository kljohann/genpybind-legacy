import pyargument_names as m

def test_constructor():
    doc = m.Something.__init__.__doc__
    try:
        val = long(5)
    except NameError: # Python 3 does not have 'long'
        val = 5
    assert ("__init__(self: pyargument_names.Something, "
            "first: int, second: bool, third: int={!r})".format(val)) in doc

def test_member_function():
    doc = m.Something.do_something.__doc__
    assert doc == (
        "do_something(self: pyargument_names.Something, "
        "some_argument: int, another_argument: float) -> None\n")
    obj = m.Something(1, False)
    assert obj.do_something.__doc__ == doc

def test_free_function():
    assert m.some_function.__doc__ == (
        "some_function(option: bool, something: bool=True) -> bool\n"
    )
