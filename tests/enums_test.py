import pytest
import pyenums as m

def test_unscoped_enum():
    assert m.test_enum(m.YES) == "Yes"
    assert m.test_enum(m.NO) == "No"
    assert m.test_enum(m.MAYBE) == "Maybe"
    assert m.YES == m.State.YES
    assert m.YES == m.State(0)
    assert sorted(m.State.__members__.keys()) == ["MAYBE", "NO", "YES"]
    assert int(m.YES) == 0 and m.YES == 0

    with pytest.raises(TypeError) as excinfo:
        m.YES | m.NO # pylint: disable=pointless-statement
    assert "unsupported operand type" in str(excinfo.value)

def test_arithmetic_enum():
    assert int(m.Access.Read | m.Access.Write | m.Access.Execute) == 7
    assert int(m.Access.Read | m.Access.Write) == 6
    assert int(m.Access.Write) == 2

    state = m.Access.Read | m.Access.Write
    assert (state & m.Access.Read) != 0
    assert (state & m.Access.Write) != 0
    assert (state & m.Access.Execute) == 0

def test_scoped_enum():
    assert m.Color(2) == m.Color.blue
    assert m.test_enum(m.Color.red) == "red"
    assert m.test_enum(m.Color.green) == "green"
    assert m.test_enum(m.Color.blue) == "blue"

    with pytest.raises(TypeError):
        m.test_enum(2)

    # FIXME: this is supposed to work but does not with pybind11 2.3
#    with pytest.raises(TypeError) as excinfo:
#        m.Color.blue == 0 # pylint: disable=pointless-statement
#    assert "incompatible function arguments" in str(excinfo.value)
#
#    with pytest.raises(TypeError) as excinfo:
#        0 == m.Color.blue # pylint: disable=pointless-statement
#    assert "incompatible function arguments" in str(excinfo.value)
#
#    with pytest.raises(TypeError) as excinfo:
#        m.Color.blue == "uiae" # pylint: disable=pointless-statement
#    assert "incompatible function arguments" in str(excinfo.value)
#
#    with pytest.raises(TypeError) as excinfo:
#        "uiae" == m.Color.blue # pylint: disable=pointless-statement
#    assert "incompatible function arguments" in str(excinfo.value)
#
#    with pytest.raises(TypeError) as excinfo:
#        m.Color.blue < 0 # pylint: disable=pointless-statement
#    assert "not supported between instances of" in str(excinfo.value)
#
#    with pytest.raises(TypeError) as excinfo:
#        0 < m.Color.blue # pylint: disable=pointless-statement
#    assert "not supported between instances of" in str(excinfo.value)

    with pytest.raises(AttributeError):
        m.blue # pylint: disable=pointless-statement
