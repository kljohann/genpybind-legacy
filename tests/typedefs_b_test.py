import pytest
import pytypedefs_b as m

# alias test in typedefs_a_test.py
def test_base():
    assert hasattr(m, 'B')
