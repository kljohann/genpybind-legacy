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

    with pytest.raises(TypeError, match="unsupported operand type"):
        m.YES | m.NO # pylint: disable=pointless-statement

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

    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.Color.blue == 0 # pylint: disable=pointless-statement

    with pytest.raises(TypeError, match="incompatible function arguments"):
        0 == m.Color.blue # pylint: disable=pointless-statement,misplaced-comparison-constant

    with pytest.raises(TypeError, match="incompatible function arguments"):
        m.Color.blue == "uiae" # pylint: disable=pointless-statement

    with pytest.raises(TypeError, match="incompatible function arguments"):
        "uiae" == m.Color.blue # pylint: disable=pointless-statement,misplaced-comparison-constant

    with pytest.raises(TypeError, match="not supported between instances of"):
        m.Color.blue < 0 # pylint: disable=pointless-statement

    with pytest.raises(TypeError, match="not supported between instances of"):
        0 < m.Color.blue # pylint: disable=pointless-statement,misplaced-comparison-constant

    assert not hasattr(m, "blue")
