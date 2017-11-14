from __future__ import unicode_literals

from .callables import Callable


class Method(Callable):
    __slots__ = (
        "_accessor_for",
    )

    # TODO: .def_property_{readonly,}_static

    def __init__(self, *args, **kwargs):
        super(Method, self).__init__(*args, **kwargs)
        self._accessor_for = {}
        if self.expose_as == "operator()":
            self.set_expose_as("__call__")

    @property
    def accessor_for(self):
        return self._accessor_for.copy()

    def set_accessor_for(self, name, access_type):
        access_type = access_type.lower()
        if access_type not in ["get", "set"]:
            raise RuntimeError(
                "invalid accessor type {!r} for property {!r}".format(access_type, name))
        existing = self._accessor_for.setdefault(name, access_type)
        if existing != access_type:
            raise RuntimeError(
                "conflicting accessor types for property {!r}: both {!r} and {!r}".format(
                    name, existing, access_type))

    def set_setter_for(self, name):
        self.set_accessor_for(name, "set")

    def set_getter_for(self, name):
        self.set_accessor_for(name, "get")
