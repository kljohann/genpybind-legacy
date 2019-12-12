import pytest
import pyvariables as m

TAGDECLS = [m.SomeStruct, m.SomeClass]

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_static_field(tagdecl):
    assert tagdecl.static_field == 1
    tagdecl.static_field = -1
    assert tagdecl.static_field == -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_static_const_field(tagdecl):
    assert tagdecl.static_const_field == 2
    with pytest.raises(AttributeError, match="can't set attribute"):
        tagdecl.static_const_field = -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_static_constexpr_field(tagdecl):
    assert tagdecl.static_constexpr_field == 3
    with pytest.raises(AttributeError, match="can't set attribute"):
        tagdecl.static_constexpr_field = -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_static_readonly_field(tagdecl):
    assert tagdecl.static_readonly_field == 4
    with pytest.raises(AttributeError, match="can't set attribute"):
        tagdecl.static_readonly_field = -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_static_writable_false_field(tagdecl):
    assert tagdecl.static_writable_false_field == 5
    with pytest.raises(AttributeError, match="can't set attribute"):
        tagdecl.static_writable_false_field = -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_field(tagdecl):
    obj = tagdecl()
    assert obj.field == 1
    obj.field = -1
    assert obj.field == -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_const_field(tagdecl):
    obj = tagdecl()
    assert obj.const_field == 2
    with pytest.raises(AttributeError, match="can't set attribute"):
        obj.const_field = -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_readonly_field(tagdecl):
    obj = tagdecl()
    assert obj.readonly_field == 4
    with pytest.raises(AttributeError, match="can't set attribute"):
        obj.readonly_field = -1

@pytest.mark.parametrize("tagdecl", TAGDECLS)
def test_writable_false_field(tagdecl):
    obj = tagdecl()
    assert obj.writable_false_field == 5
    with pytest.raises(AttributeError, match="can't set attribute"):
        obj.writable_false_field = -1

def test_global_variables():
    assert m.var == 1
    m.var = -1
    assert m.var == -1
    assert m.const_var == 2

@pytest.mark.xfail(reason="not enforceable")
def test_global_const_variable_is_readonly():
    with pytest.raises(AttributeError, match="can't set attribute"):
        m.const_var = -1
