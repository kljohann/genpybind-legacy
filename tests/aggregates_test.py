import pytest
import pyaggregates as m

@pytest.mark.skip(reason="not implemented")
def test_aggregate_does_not_have_default_ctor():
    with pytest.raises(TypeError) as excinfo:
        obj = m.Aggregate()  # pylint: disable=unused-variable
    assert "incompatible constructor arguments" in str(excinfo.value)

@pytest.mark.skip(reason="not implemented")
def test_aggregate_has_ctor():
    obj = m.Aggregate(1, 2, 3)
    assert obj.a == 1
    assert obj.b == 2
    assert obj.c == 3

@pytest.mark.skip(reason="not implemented")
def test_aggregate_has_copy_ctor():
    obj = m.Aggregate(1, 2, 3)
    obj_copy = m.Aggregate(obj)
    assert obj_copy.a == 1
    assert obj_copy.b == 2
    assert obj_copy.c == 3
