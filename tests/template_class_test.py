import pytest
import pytemplate_class as m

def test_templated_typedef():
    assert getattr(m.TBase_int, 'do_something', False)

