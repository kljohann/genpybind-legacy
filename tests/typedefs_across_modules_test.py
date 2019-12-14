import pytypedefs_across_modules as m

def test_alias_is_available():
    instance = m.alias()
    instance_of_typedef = m.alias_for_typedef()

    # The module containing the definition is only included here to check the
    # identity of the type.
    import pytypedefs_definition  # pylint: disable=import-outside-toplevel

    assert isinstance(instance, pytypedefs_definition.Definition)
    assert isinstance(instance_of_typedef, pytypedefs_definition.Definition)

def test_definition_does_not_spill_into_this_module():
    assert not hasattr(m, "Definition")
    assert not hasattr(m, "Typedef")
