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
    assert not hasattr(m, "OnlyInB")
