from __future__ import unicode_literals

from clang.cindex import TokenKind

from .. import cutils
from .declarations import Declaration


class Manual(Declaration):
    __slots__ = (
        "_code",
        "_postamble",
    )

    def __init__(self, *args, **kwargs):
        self._code = kwargs.pop("code", None)
        super(Manual, self).__init__(*args, **kwargs)
        self._postamble = False

    @property
    def visible(self):
        return True

    @property
    def code(self):
        return self._code

    @property
    def postamble(self):
        return self._postamble

    def set_postamble(self):
        self._postamble = True

    def set_manual(self):
        pass

    def statements(self, parent, registry):
        if self.postamble:
            yield (self, parent)
        else:
            for result in self.expose_later(None, parent, registry):
                yield result

    def expose_later(self, _, parent, _registry):
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
