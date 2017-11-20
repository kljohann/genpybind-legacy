import pytest
import pyrequired as m

def test_nullptr():
    p = m.Parent()
    p.accept(m.Child())
    p.accept(None)

@pytest.mark.skip(reason="not implemented")
def test_required():
    p = m.Parent()
    p.required(m.Child())
    p.required(None)
