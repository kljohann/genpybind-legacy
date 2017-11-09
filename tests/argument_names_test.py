import pytest
import pyargument_names as m

def test_constructor():
    doc = m.Something.__init__.__doc__
    assert ("__init__(self: pyargument_names.Something, "
            "first: int, second: bool, third: int=5L)") in doc

def test_member_function():
    doc = m.Something.do_something.__doc__
    assert doc == (
        "do_something(self: pyargument_names.Something, "
        "some_argument: int, another_argument: float) -> None\n")
    x = m.Something(1, False)
    assert x.do_something.__doc__ == doc

def test_free_function():
    assert m.some_function.__doc__ == (
        "some_function(option: bool, something: bool=True) -> bool\n"
    )
