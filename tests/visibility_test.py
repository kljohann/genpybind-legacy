import pytest
import pyvisibility as m

def test_unannotated():
    with pytest.raises(AttributeError):
        m.Unannotated

def test_hidden():
    with pytest.raises(AttributeError):
        m.Hidden

def test_visible():
    klass = m.Visible()
    assert klass.public_constant == True
    with pytest.raises(AttributeError):
        klass.hidden_public_constant
    with pytest.raises(AttributeError):
        klass.protected_constant
    with pytest.raises(AttributeError):
        klass.private_constant

def test_unannotated_in_namespace():
    with pytest.raises(AttributeError):
        m.UnannotatedInNamespace

def test_unannotated_in_visible_namespace():
    klass = m.UnannotatedInVisibleNamespace()

def test_visible_in_visible_namespace():
    klass = m.VisibleInVisibleNamespace()

def test_visible_false_in_visible_namespace():
    with pytest.raises(AttributeError):
        m.VisibleFalseInVisibleNamespace

def test_visible_default_in_visible_namespace():
    klass = m.VisibleDefaultInVisibleNamespace()

def test_hidden_in_visible_namespace():
    with pytest.raises(AttributeError):
        m.HiddenInVisibleNamespace

def test_unannotated_in_namespace_in_visible_namespace():
    klass = m.UnannotatedInNamespaceInVisibleNamespace()

def test_unannotated_in_hidden_namespace_in_visible_namespace():
    with pytest.raises(AttributeError):
        m.UnannotatedInHiddenNamespaceInVisibleNamespace

def test_default_visibility_for_exposed_elsewhere():
    with pytest.raises(AttributeError):
        m.UsedIndirectly

    klass = m.SomeScope.ExposedHere()
    assert klass.should_be_visible == True
    assert m.SomeScope.ExposedHere.should_be_visible == True

    with pytest.raises(AttributeError):
        m.SomeScope.ExposedHere.should_be_hidden

    with pytest.raises(AttributeError):
        klass.should_be_hidden
