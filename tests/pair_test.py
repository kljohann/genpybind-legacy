import pytest
import pypair as m

def test_pair_of_floats():
    assert hasattr(m, 'my_float_pair')
    assert hasattr(m.my_float_pair, 'first')
    assert hasattr(m.my_float_pair, 'second')
    assert hasattr(m.my_float_pair, 'swap')
    assert hasattr(m, 'generate_float_pair')
    fp = m.generate_float_pair()
    assert fp.first == pytest.approx(0.1)
    assert fp.second == pytest.approx(1.1)
    fp2 = m.my_float_pair(fp)
    assert fp2.first == pytest.approx(0.1)
    assert fp2.second == pytest.approx(1.1)

