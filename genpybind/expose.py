import textwrap


from . import utils
from .registry import Registry
from .utils import quote

if False:  # pylint: disable=using-constant-test
    from .decls.declarations import Declaration  # pylint: disable=unused-import
    from typing import (  # pylint: disable=unused-import
        List, Optional, Text, Tuple, Union)


def expose_as(
        toplevel_declarations,  # type: List[Declaration]
        module,  # type: Text
        doc=None,  # type: Optional[Text]
        isystem=None,  # type: Optional[List[Text]]
        includes=None,  # type: Optional[List[Text]]
        tags=None,  # type: Optional[List[Text]]
):
    # type: (...) -> Text
    tpl = textwrap.dedent("""
    #include <sstream>
    #include <pybind11/pybind11.h>
    #include <pybind11/stl.h>
    {isystem}

    {includes}

    namespace py = pybind11;

    template <typename T>
    struct genpybind_stringstream_helper
    {{
        std::string operator()(T const& value) const {{
            std::stringstream tmp;
            tmp << value;
            return tmp.str();
        }}
    }};

    // If `T` is registered with pybind11 the corresponding Python type is returned.
    // Else a warning is emitted and None is returned.
    template <typename T>
    py::object genpybind_get_type_object() {{
        std::type_info const &tp = typeid(T);
        auto tinfo = py::detail::get_type_info(tp, /*throw_if_missing=*/false);
        if (!tinfo) {{
            std::string name = tp.name();
            py::detail::clean_type_id(name);
            PyErr_WarnFormat(PyExc_Warning, /*stack_level=*/7,
                             "Reference to unknown type '%s'", name.c_str());
            return pybind11::none();
        }}
        return py::reinterpret_borrow<py::object>((PyObject *)tinfo->type);
    }}

    PYBIND11_MODULE({module}, {var}) {{
    {var}.doc() = {doc};
    {statements}
    }}
    """).strip()

    var = "m"
    registry = Registry(tags=tags)

    statements = []  # type: List[Text]
    pending_declarations = []  # type: List[Tuple[Declaration, Text]]
    postamble_declarations = []  # type: List[Tuple[Declaration, Text]]

    def handle_return(declaration, value, postamble_only=False):
        # type: (Declaration, Union[None, Text, Tuple[Declaration, Text]], bool) -> None
        """
        expose() may either yield a string containing a statement to be emitted or
        a pair of a declaration and the identifier of the parent scope to use.
        In the latter case it will be added to a list of pending declarations on which
        expose_later() is called after all other normal declarations have been processed.
        If in addition the returned declaration has a truthy "postamble" attribute, it
        will be processed even later.
        """
        if value is None:
            return
        if not isinstance(value, tuple):
            assert isinstance(value, str)
            statements.append(value)
            return
        declaration, _ = value
        is_postamble = getattr(declaration, "postamble", None)
        if postamble_only or is_postamble:
            postamble_declarations.append(value)
            return
        pending_declarations.append(value)

    for declaration in toplevel_declarations:
        for value in utils.flatten(declaration.expose(var, registry)):
            handle_return(declaration, value)

    while pending_declarations:
        declaration, parent = pending_declarations.pop(0)
        for value in utils.flatten(declaration.expose_later(var, parent, registry)):
            handle_return(declaration, value)

    while postamble_declarations:
        declaration, parent = postamble_declarations.pop(0)
        for value in utils.flatten(declaration.expose_later(var, parent, registry)):
            handle_return(declaration, value, postamble_only=True)

    return tpl.format(
        module=module,
        name=quote(module),
        doc=quote(doc),
        isystem="\n".join('#include <{}>'.format(f) for f in isystem or []),
        includes="\n".join('#include {}'.format(quote(f)) for f in includes or []),
        var=var,
        statements="\n".join(statement for statement in statements),
    )
