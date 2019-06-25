import pytest
import pytypedefs_a as m
import pytypedefs_b as m_b

def test_alias():
    assert hasattr(m, 'typedef_A')
    assert isinstance(m.typedef_A(), m.A)
    assert hasattr(m, 'typedef_B')
    assert isinstance(m.typedef_B(), m_b.B)
