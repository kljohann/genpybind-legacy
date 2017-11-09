import pykeep_alive as m

class Counter(object):
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

children = Counter(m.Child)
parents = Counter(m.Parent)

def test_sink_unannotated():
    children.reset()
    parents.reset()

    p = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    m.Child()
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0
    p.sink(m.Child())
    assert children.created == 2
    assert children.destroyed == 2
    assert children.alive == 0

    del p
    assert parents.alive == 0

def test_sink_keep_alive():
    children.reset()
    parents.reset()

    p = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    assert children.alive == 0
    p.sink_keep_alive(m.Child())
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del p
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_sink_keep_alive_plain():
    children.reset()
    parents.reset()

    p = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    assert children.alive == 0
    p.sink_keep_alive_plain(m.Child())
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del p
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_source_unannotated():
    children.reset()
    parents.reset()

    p = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    p.source()
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

    del p
    assert parents.alive == 0

def test_source_keep_alive():
    children.reset()
    parents.reset()

    p = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    p.source_keep_alive()
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del p
    assert parents.alive == 0
    assert children.created == 1
    assert children.destroyed == 1
    assert children.alive == 0

def test_source_keep_alive_parent():
    children.reset()
    parents.reset()

    p = m.Parent()
    assert parents.alive == 1

    assert children.created == 0
    assert children.destroyed == 0
    c = p.source_keep_alive_parent()
    assert children.created == 1
    assert children.destroyed == 0
    assert children.alive == 1

    del p
    assert parents.alive == 1
    assert children.alive == 1

    del c
    assert parents.alive == 0
    assert children.alive == 0
