import pytest
import pyimplicit_conversion as m

def test_from_class_implicit_without_annotation():
    with pytest.raises(TypeError) as excinfo:
        m.test_value(m.One())
    assert "incompatible function arguments" in str(excinfo.value)

def test_from_class_explicit_without_annotation():
    with pytest.raises(TypeError) as excinfo:
        m.test_value(m.Two())
    assert "incompatible function arguments" in str(excinfo.value)

def test_from_class_implicit_with_annotation():
    m.test_value(m.Three())

def test_from_pod_explicit_without_annotation():
    with pytest.raises(TypeError) as excinfo:
        m.test_value(2.0)
    assert "incompatible function arguments" in str(excinfo.value)

def test_from_pod_implicit_with_annotation():
    m.test_value(42)
