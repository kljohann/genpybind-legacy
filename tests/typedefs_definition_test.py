import pytypedefs_definition as m


def test_definition_is_available_locally():
    assert hasattr(m, "Definition")
    assert hasattr(m, "Typedef")
    assert hasattr(m.Definition, "NestedDefinition")
    assert hasattr(m.Definition, "NestedTypedef")
    assert hasattr(m, "Typedef")
