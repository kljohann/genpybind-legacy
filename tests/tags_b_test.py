import pytest
import pytags_b as m

def test_tags():
    m.Everywhere()
    m.OnlyInB()
    m.OnlyInAB()
    m.EverywhereInTests()
    m.NamespacedOnlyInAB()
    m.NamespacedEverywhere()
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInA
    assert "has no attribute" in str(excinfo.value)
