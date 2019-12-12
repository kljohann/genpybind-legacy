import pyvisibility as m

def test_unannotated():
    assert not hasattr(m, "Unannotated")

def test_hidden():
    assert not hasattr(m, "Hidden")

def test_visible():
    klass = m.Visible()
    assert klass.public_constant is True
    assert not hasattr(klass, "hidden_public_constant")
    assert not hasattr(klass, "protected_constant")
    assert not hasattr(klass, "private_constant")

def test_unannotated_in_namespace():
    assert not hasattr(m, "UnannotatedInNamespace")

def test_unannotated_in_visible_namespace():
    _klass = m.UnannotatedInVisibleNamespace()

def test_visible_in_visible_namespace():
    _klass = m.VisibleInVisibleNamespace()

def test_visible_false_in_visible_namespace():
    assert not hasattr(m, "VisibleFalseInVisibleNamespace")

def test_visible_default_in_visible_namespace():
    _klass = m.VisibleDefaultInVisibleNamespace()

def test_hidden_in_visible_namespace():
    assert not hasattr(m, "HiddenInVisibleNamespace")

def test_unannotated_in_namespace_in_visible_namespace():
    _klass = m.UnannotatedInNamespaceInVisibleNamespace()

def test_unannotated_in_hidden_namespace_in_visible_namespace():
    assert not hasattr(m, "UnannotatedInHiddenNamespaceInVisibleNamespace")

def test_default_visibility_for_exposed_elsewhere():
    assert not hasattr(m, "UsedIndirectly")

    klass = m.SomeScope.ExposedHere()
    assert klass.should_be_visible is True
    assert m.SomeScope.ExposedHere.should_be_visible is True

    assert not hasattr(m.SomeScope.ExposedHere, "should_be_hidden")
    assert not hasattr(klass, "should_be_hidden")
