import pytest
import pytags_c as m

def test_tags():
    m.Everywhere()
    m.EverywhereInTests()
    m.NamespacedEverywhere()
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInA
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInB
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInAB
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.NamespacedOnlyInAB
    assert "has no attribute" in str(excinfo.value)
