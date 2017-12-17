from __future__ import unicode_literals

from clang.cindex import TokenKind

from .. import cutils
from .declarations import Declaration

if False:  # pylint: disable=using-constant-test
    from clang import cindex  # pylint: disable=unused-import
    from ..registry import Registry  # pylint: disable=unused-import
    from typing import Any, Iterable, List, Optional, Text, Tuple, Union  # pylint: disable=unused-import


class Manual(Declaration):
    __slots__ = (
        "_code",
        "_postamble",
    )

    def __init__(self, cursor, code=None, **kwargs):
        # type: (cindex.Cursor, Optional[cindex.Cursor], **Any) -> None
        assert code is not None
        self._code = code
        super(Manual, self).__init__(cursor, **kwargs)
        self._postamble = False

    @property
    def visible(self):
        # type: () -> bool
        return True

    @property
    def code(self):
        # type: () -> cindex.Cursor
        return self._code

    @property
    def postamble(self):
        # type: () -> bool
        return self._postamble

    def set_postamble(self):
        # type: () -> None
        self._postamble = True

    def set_manual(self):
        # type: () -> None
        pass

    def statements(self, parent, registry):
        # type: (Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        if self.postamble:
            yield (self, parent)
        else:
            for result in self.expose_later("", parent, registry):
                yield result

    def expose_later(self, _toplevel, parent, _registry):
        # type: (Text, Text, Registry) -> Iterable[Union[Tuple[Declaration, Text], Text]]
        output = []
        tokens = list(cutils.get_tokens_with_whitespace(self.code))

        while tokens:
            token = tokens.pop(0)
            if token.kind == TokenKind.IDENTIFIER:
                # GENPYBIND_PARENT_TYPE is a fill in for the parent type, which is incomplete when
                # defining the lambda that is used to capture the manual wrapping code.
                if token.spelling == "GENPYBIND_PARENT_TYPE":
                    output.append(cutils.fully_qualified_name(self.parent_cursor))
                    continue

                # Translate "parent" to appropriate identifier.  Also remove any instance of
                # "parent->".  The resulting dependent name allows us to introduce expressions
                # referring to things which are only in scope in the definition of the bindings but
                # not in the header file, e.g. "parent->py::module".
                if token.spelling == "parent":
                    if tokens and tokens[0].spelling == "->":
                        tokens.pop(0)
                        # To obtain "py::class_<...>" we have to write "parent->py::template class_<...>",
                        # because "class_" has to be treated as a dependent template name.
                        if tokens and tokens[0].spelling == "template":
                            # ignore
                            tokens.pop(0)
                    else:
                        output.append(parent)
                    continue

            output.append(token.spelling)

        yield "".join(output)
