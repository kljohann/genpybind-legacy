import pytest
import pytags_b as m

def test_tags():
    m.Everywhere()
    m.OnlyInB()
    m.OnlyInAB()
    m.EverywhereInTests()
    m.NamespacedOnlyInAB()
    m.NamespacedEverywhere()
    m.NestedSubmoduleOnlyInAB.X()
    m.NestedSubmoduleOnlyInAB.AlsoOnlyInAB()
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInA # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
