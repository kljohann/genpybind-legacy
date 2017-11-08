import pytest
import pysubmodules as m

def test_submodule():
    with pytest.raises(AttributeError):
        m.X
    x = m.submodule.X()
    assert "pysubmodules.submodule.X" in repr(x)

def test_visible_submodule():
    x = m.submodule_.X()
    assert "pysubmodules.submodule_.X" in repr(x)

def test_named_submodule():
    x = m.named.X()
    assert "pysubmodules.named.X" in repr(x)

def test_submodule_expose_as():
    x = m.expose_as.X()
    assert "pysubmodules.expose_as.X" in repr(x)

def test_submodule_named_expose_as():
    with pytest.raises(AttributeError):
        m.ignored
    x = m.xyz.X()
    assert "pysubmodules.xyz.X" in repr(x)
