import pyinline_base_crtp as m

def test_crtp_enum():
    assert m.Enum().value() == 0
    obj = m.Enum(42)
    obj2 = m.Enum(128)
    assert obj == obj
    assert obj != obj2
    assert obj < obj2
    assert obj <= obj2
    assert obj <= obj
    assert obj2 > obj
    assert obj2 >= obj
    assert obj >= obj
    assert obj.value() == 42
    assert int(obj) == 42
    assert str(obj) == "[42]"
    assert repr(obj) == "[42]"
    assert hash(obj) == 42
