import pysubmodules as m

def test_submodule():
    assert not hasattr(m, "X")
    obj = m.submodule.X()
    assert "pysubmodules.submodule.X" in repr(obj)

def test_visible_submodule():
    obj = m.submodule_.X()
    assert "pysubmodules.submodule_.X" in repr(obj)

def test_named_submodule():
    obj = m.named.X()
    assert "pysubmodules.named.X" in repr(obj)

def test_submodule_expose_as():
    obj = m.expose_as.X()
    assert "pysubmodules.expose_as.X" in repr(obj)

def test_submodule_named_expose_as():
    assert not hasattr(m, "ignored")
    obj = m.xyz.X()
    assert "pysubmodules.xyz.X" in repr(obj)
