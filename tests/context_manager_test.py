import pytest
import pycontext_manager as m

def test_context_manager():

    assert m.get_global_instance_counter() == 42

    with m.ProxyRAII() as pr:
        assert m.get_global_instance_counter() == 43

    with m.ProxyRAII() as pr:
        assert m.get_global_instance_counter() == 43

    assert m.get_global_instance_counter() == 42
