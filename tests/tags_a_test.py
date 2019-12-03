import pytest
import pytags_a as m

def test_tags():
    m.Everywhere()
    m.OnlyInA()
    m.OnlyInAB()
    m.EverywhereInTests()
    m.NamespacedOnlyInAB()
    m.NamespacedEverywhere()
    m.NestedSubmoduleOnlyInAB.X()
    m.NestedSubmoduleOnlyInAB.AlsoOnlyInAB()
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInB # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
