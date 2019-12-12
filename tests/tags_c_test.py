import pytags_c as m

def test_tags():
    m.Everywhere()
    m.EverywhereInTests()
    m.NamespacedEverywhere()
    assert not hasattr(m, "OnlyInA")
    assert not hasattr(m, "OnlyInB")
    assert not hasattr(m, "OnlyInAB")
    assert not hasattr(m, "NamespacedOnlyInAB")
    assert not hasattr(m, "NestedSubmoduleOnlyInAB")
    assert not hasattr(m, "AlsoOnlyInAB")
