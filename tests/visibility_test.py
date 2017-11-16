import pytest
import pyvisibility as m

def test_unannotated():
    with pytest.raises(AttributeError):
        m.Unannotated # pylint: disable=pointless-statement

def test_hidden():
    with pytest.raises(AttributeError):
        m.Hidden # pylint: disable=pointless-statement

def test_visible():
    klass = m.Visible()
    assert klass.public_constant is True
    with pytest.raises(AttributeError):
        klass.hidden_public_constant # pylint: disable=pointless-statement
    with pytest.raises(AttributeError):
        klass.protected_constant # pylint: disable=pointless-statement
    with pytest.raises(AttributeError):
        klass.private_constant # pylint: disable=pointless-statement

def test_unannotated_in_namespace():
    with pytest.raises(AttributeError):
        m.UnannotatedInNamespace # pylint: disable=pointless-statement

def test_unannotated_in_visible_namespace():
    _klass = m.UnannotatedInVisibleNamespace()

def test_visible_in_visible_namespace():
    _klass = m.VisibleInVisibleNamespace()

def test_visible_false_in_visible_namespace():
    with pytest.raises(AttributeError):
        m.VisibleFalseInVisibleNamespace # pylint: disable=pointless-statement

def test_visible_default_in_visible_namespace():
    _klass = m.VisibleDefaultInVisibleNamespace()

def test_hidden_in_visible_namespace():
    with pytest.raises(AttributeError):
        m.HiddenInVisibleNamespace # pylint: disable=pointless-statement

def test_unannotated_in_namespace_in_visible_namespace():
    _klass = m.UnannotatedInNamespaceInVisibleNamespace()

def test_unannotated_in_hidden_namespace_in_visible_namespace():
    with pytest.raises(AttributeError):
        m.UnannotatedInHiddenNamespaceInVisibleNamespace # pylint: disable=pointless-statement

def test_default_visibility_for_exposed_elsewhere():
    with pytest.raises(AttributeError):
        m.UsedIndirectly # pylint: disable=pointless-statement

    klass = m.SomeScope.ExposedHere()
    assert klass.should_be_visible is True
    assert m.SomeScope.ExposedHere.should_be_visible is True

    with pytest.raises(AttributeError):
        m.SomeScope.ExposedHere.should_be_hidden # pylint: disable=pointless-statement

    with pytest.raises(AttributeError):
        klass.should_be_hidden # pylint: disable=pointless-statement
