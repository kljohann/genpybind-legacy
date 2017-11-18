import operator

import pytest
import pyoperators as m

BINARY_OPERATORS = "lt le eq ne gt ge".split()

@pytest.mark.parametrize("variant", ["member", "friend"])
@pytest.mark.parametrize("name", BINARY_OPERATORS)
def test_has_binary_operator(variant, name):
    obj = getattr(m, "has_{}_{}".format(variant, name))()
    assert hasattr(obj, "__{}__".format(name))
    assert getattr(operator, name)(obj, obj) is True

@pytest.mark.parametrize("variant", ["hidden", "private", "hidden_friend"])
@pytest.mark.parametrize("name", BINARY_OPERATORS)
def test_has_no_binary_operator(variant, name):
    obj = getattr(m, "has_{}_{}".format(variant, name))()
    if name in ["eq", "ne"]:
        # TODO: sadly, python seems to synthesize a default function in the absence of __eq__ or __ne__ :(
        return
    with pytest.raises(TypeError) as excinfo:
        getattr(operator, name)(obj, obj)
    assert "not supported between instances of" in str(excinfo.value)
