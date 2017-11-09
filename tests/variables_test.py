import pytest
import pyvariables as m

tagdecls = [m.SomeStruct, m.SomeClass]

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_static_field(tagdecl):
    assert tagdecl.static_field == 1
    tagdecl.static_field = -1
    assert tagdecl.static_field == -1

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_static_const_field(tagdecl):
    assert tagdecl.static_const_field == 2
    with pytest.raises(AttributeError) as excinfo:
        tagdecl.static_const_field = -1
    assert "can't set attribute" in str(excinfo.value)

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_static_constexpr_field(tagdecl):
    assert tagdecl.static_constexpr_field == 3
    with pytest.raises(AttributeError) as excinfo:
        tagdecl.static_constexpr_field = -1
    assert "can't set attribute" in str(excinfo.value)

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_static_readonly_field(tagdecl):
    assert tagdecl.static_readonly_field == 4
    with pytest.raises(AttributeError) as excinfo:
        tagdecl.static_readonly_field = -1
    assert "can't set attribute" in str(excinfo.value)

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_static_writable_false_field(tagdecl):
    assert tagdecl.static_writable_false_field == 5
    with pytest.raises(AttributeError) as excinfo:
        tagdecl.static_writable_false_field = -1
    assert "can't set attribute" in str(excinfo.value)

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_field(tagdecl):
    x = tagdecl()
    assert x.field == 1
    x.field = -1
    assert x.field == -1

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_const_field(tagdecl):
    x = tagdecl()
    assert x.const_field == 2
    with pytest.raises(AttributeError) as excinfo:
        x.const_field = -1
    assert "can't set attribute" in str(excinfo.value)

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_readonly_field(tagdecl):
    x = tagdecl()
    assert x.readonly_field == 4
    with pytest.raises(AttributeError) as excinfo:
        x.readonly_field = -1
    assert "can't set attribute" in str(excinfo.value)

@pytest.mark.parametrize("tagdecl", tagdecls)
def test_writable_false_field(tagdecl):
    x = tagdecl()
    assert x.writable_false_field == 5
    with pytest.raises(AttributeError) as excinfo:
        x.writable_false_field = -1
    assert "can't set attribute" in str(excinfo.value)

def test_global_variables():
    assert m.var == 1
    m.var = -1
    assert m.var == -1
    assert m.const_var == 2

@pytest.mark.xfail(reason="not enforceable")
def test_global_const_variable_is_readonly():
    with pytest.raises(AttributeError) as excinfo:
        m.const_var = -1
    assert "can't set attribute" in str(excinfo.value)
