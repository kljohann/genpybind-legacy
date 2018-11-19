import pytest
import pyoptional_parameters as m

def test_optional_parameters():
    assert hasattr(m, 'foo')
    assert m.foo(0) == 0
    assert m.foo(10) == 10
    assert m.foo(None) is None
    assert m.foo() is None
