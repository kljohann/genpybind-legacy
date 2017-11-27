import pytest
import pyrequired as m

def test_nullptr():
    obj = m.Parent()
    obj.accept(m.Child())
    obj.accept(None)

def test_required():
    obj = m.Parent()
    obj.required(m.Child())
    with pytest.raises(TypeError) as excinfo:
        obj.required(None)
    assert "incompatible function arguments" in str(excinfo.value)
