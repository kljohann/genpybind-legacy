from .declarations import Declaration

if False:  # pylint: disable=using-constant-test
    from typing import (Any, List, Tuple)  # pylint: disable=unused-import


class Level(Declaration):
    __slots__ = (
        "_children",
    )

    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        super(Level, self).__init__(*args, **kwargs)
        self._children = []  # type: List[Declaration]

    @property
    def children(self):
        # type: () -> Tuple[Declaration, ...]
        return tuple(self._children)

    def add_child(self, declaration):
        # type: (Declaration) -> None
        assert isinstance(declaration, Declaration)
        self._children.append(declaration)
