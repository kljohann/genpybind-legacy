import pykeep_alive as m

class Counter:
    def __init__(self, klass):
        self.klass = klass
        self.reset()

    def reset(self):
        self._created = self.klass.created
        self._destroyed = self.klass.destroyed

    @property
    def alive(self):
        return self.created - self.destroyed

    @property
    def created(self):
        return self.klass.created - self._created

    @property
    def destroyed(self):
        return self.klass.destroyed - self._destroyed

children = Counter(m.Child) # pylint: disable=invalid-name
parents = Counter(m.Parent) # pylint: disable=invalid-name

def test_sink_unannotated():
    children.reset()
    parents.reset()

    parent = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    m.Child()
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0
    parent.sink(m.Child())
    assert children.created == 2
    assert children.destroyed == 2
    assert children.alive == 0

    del parent
    assert parents.alive == 0

def test_ctor_keep_alive():
    children.reset()
    parents.reset()

    assert children.created == 0
    assert children.destroyed == 0
    assert children.alive == 0
    assert parents.alive == 0
    parent = m.Parent(m.Child())
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1
    assert parents.alive == 1

    del parent
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_sink_keep_alive():
    children.reset()
    parents.reset()

    parent = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    assert children.alive == 0
    parent.sink_keep_alive(m.Child())
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del parent
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_sink_keep_alive_plain():
    children.reset()
    parents.reset()

    parent = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    assert children.alive == 0
    parent.sink_keep_alive_plain(m.Child())
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del parent
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_source_unannotated():
    children.reset()
    parents.reset()

    parent = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    parent.source()
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

    del parent
    assert parents.alive == 0

def test_source_keep_alive():
    children.reset()
    parents.reset()

    parent = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    parent.source_keep_alive()
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del parent
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_source_keep_alive_parent():
    children.reset()
    parents.reset()

    parent = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    child = parent.source_keep_alive_parent()
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del parent
    assert parents.alive == 1
    assert children.alive == 1

    del child
    assert parents.alive == 0
    assert children.alive == 0
