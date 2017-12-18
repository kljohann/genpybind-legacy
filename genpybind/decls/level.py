from .declarations import Declaration


class Level(Declaration):
    __slots__ = (
        "_children",
    )

    def __init__(self, *args, **kwargs):
        super(Level, self).__init__(*args, **kwargs)
        self._children = []

    @property
    def children(self):
        return tuple(self._children)

    def add_child(self, declaration):
        assert isinstance(declaration, Declaration)
        self._children.append(declaration)
