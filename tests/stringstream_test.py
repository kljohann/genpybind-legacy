import pystringstream as m

def test_friend_ostream():
    obj = m.Something()
    assert str(obj) == "uiae"
    assert repr(obj) == "uiae"
