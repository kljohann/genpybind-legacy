import pyholder_type as h
import pytest


def test_shared_ptr():
    p = h.Parent()
    c0 = p.get_use_count()
    assert c0 == 1
    sp1 = p.get_child()
    c1 = p.get_use_count()
    assert c1 == 2
    assert sp1 == p.get_child()
    del sp1
    c2 = p.get_use_count()
    assert c2 == 1
