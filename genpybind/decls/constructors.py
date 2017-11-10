from .. import cutils, utils
from ..utils import join_arguments, quote
from .methods import Method


class Constructor(Method):
    __slots__ = (
        "_implicit_conversion",
    )

    def __init__(self, *args, **kwargs):
        super(Constructor, self).__init__(*args, **kwargs)
        self._implicit_conversion = False

    @property
    def implicit_conversion(self):
        return self._implicit_conversion

    def set_implicit_conversion(self, value=True):
        self._implicit_conversion = bool(value)

    def set_return_value_policy(self, value):
        raise RuntimeError(
            "return_value_policy not supported for constructors")

    def statements(self, parent, registry):
        if self.implicit_conversion:
            yield (self, parent)

        if self.cursor.semantic_parent.is_abstract_record():
            return

        if self.cursor.is_move_constructor():
            return

        yield "{parent}.def({args});".format(
            parent=parent,
            args=join_arguments(
                "py::init<{}>()".format(join_arguments(self.argument_types())),
                quote(self.cursor.brief_comment),
                self.arguments(),
                self.policies(),
            )
        )

    def expose_later(self, toplevel, parent, registry):
        argument_type = next(iter(self.cursor.type.argument_types()))
        if cutils.is_valid_type(argument_type.get_pointee()):
                argument_type = argument_type.get_pointee()
        # TODO: Retrieve non-const-qualified type
        record_type = self.parent_cursor.type
        yield "py::implicitly_convertible<{}>();".format(join_arguments(
            utils.strip_prefix(argument_type.fully_qualified_name, "const "),
            record_type.fully_qualified_name,
        ))
