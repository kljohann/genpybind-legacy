import pytest
import pyarray as m

def test_array_of_floats():
    assert hasattr(m, 'Something')
    a = m.Something()
    for i in range(len(a)):
        a[i] = i
    for i in range(len(a)):
        assert a[i] == i
