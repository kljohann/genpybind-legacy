import pyargsandkwargs as m

def test_args():
    assert m.test_args() == 0
    assert m.test_args(0,1,2,3) == 4

def test_kwargs():
    assert m.test_kwargs() == 0
    assert m.test_kwargs(abc=[0,1,2,3]) == 4

def test_overloads():
    assert m.test() == 0
    assert m.test(abc=[0,1,2,3]) == 4
    assert m.test(1, 0.1) == 2
    assert m.test(1, 0.1, 0, 1, 2, 3) == 6
    assert m.test(1, 0.1, abc=[0,1,2,3]) == 4
    assert m.test(1, 0.1, 0, 1, 2, abc=[0,1,2,3]) == 7
