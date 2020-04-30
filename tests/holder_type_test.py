import pyholder_type as h


def test_shared_ptr():
    parent = h.Parent()
    assert parent.get_use_count() == 1
    shared_child1 = parent.get_child()
    assert parent.get_use_count() == 2
    assert shared_child1 == parent.get_child()
    del shared_child1
    assert parent.get_use_count() == 1
