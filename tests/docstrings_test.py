import pytest
import pydocstrings as m

def test_constructor():
    assert "The default constructor!" in m.Something.__init__.__doc__

def test_member_function():
    assert "A member function!" in m.Something.do_something.__doc__
    obj = m.Something()
    assert obj.do_something.__doc__ == m.Something.do_something.__doc__

def test_operator():
    assert "A comparison operator!" in m.Something.__eq__.__doc__
    obj = m.Something()
    assert obj.__eq__.__doc__ == m.Something.__eq__.__doc__

def test_friend_operator_inline_definition():
    assert "Inline friend!" in m.Something.__ne__.__doc__
    obj = m.Something()
    assert obj.__ne__.__doc__ == m.Something.__ne__.__doc__

def test_friend_operator():
    assert "Less than!" in m.Something.__lt__.__doc__
    obj = m.Something()
    assert obj.__lt__.__doc__ == m.Something.__lt__.__doc__

def test_free_function():
    assert "A free function!" in m.some_function.__doc__

# Apparently brief_comment contains not just the \brief part...
@pytest.mark.xfail(reason="semantics of brief_comment in libclang")
def test_docstrings_are_brief():
    assert "More documentation here." not in m.Something.__init__.__doc__
    assert "More documentation here." not in m.Something.do_something.__doc__
    assert "More documentation here." not in m.some_function.__doc__
    assert "More documentation here." not in m.Something.__eq__.__doc__
    assert "More documentation here." not in m.Something.__ne__.__doc__
    assert "More documentation here." not in m.Something.__lt__.__doc__
