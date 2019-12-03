import pytest
import pytags_c as m

def test_tags():
    m.Everywhere()
    m.EverywhereInTests()
    m.NamespacedEverywhere()
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInA # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInB # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.OnlyInAB # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.NamespacedOnlyInAB # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.NestedSubmoduleOnlyInAB # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        m.AlsoOnlyInAB # pylint: disable=pointless-statement
    assert "has no attribute" in str(excinfo.value)
