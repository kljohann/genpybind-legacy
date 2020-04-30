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
    assert not hasattr(m, "OnlyInA")
