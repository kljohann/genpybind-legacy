import pytest


@pytest.fixture(scope="session")
def module_with_warnings():
    """Capture warnings when importing the module for use in tests below."""
    with pytest.warns(None) as recorder:
        import pytypedefs as m  # pylint: disable=import-outside-toplevel
    yield m, recorder
    # Check that there were no unexpected warnings (see use of `.pop()` below).
    assert len(recorder) == 0


@pytest.fixture(params=[None, "VisibleParent"])
# pylint: disable=redefined-outer-name
def parent(module_with_warnings, request):
    m, _ = module_with_warnings
    return m if request.param is None else getattr(m, request.param)


@pytest.mark.parametrize("feature", ["using", "typedef"])
# pylint: disable=redefined-outer-name
def test_visibility(module_with_warnings, parent, feature):
    m, _ = module_with_warnings
    for variant in ["explicitly_visible", "implicitly_visible"]:
        assert getattr(parent, "{}_{}".format(feature, variant)) is m.Target

    for variant in ["not_visible", "explicitly_hidden"]:
        assert not hasattr(parent, "{}_{}".format(feature, variant))


@pytest.mark.parametrize("feature", ["using", "typedef"])
# pylint: disable=redefined-outer-name
def test_unexposed_target(module_with_warnings, parent, feature):
    m, warnings_recorder = module_with_warnings

    assert not hasattr(m, "UnexposedTarget")
    assert getattr(parent, "{}_unexposed_target".format(feature)) is None

    # A warning is expected to be emitted for each alias.  As the text of the
    # warning is the same in this case, we can just pop and check any warning
    # message to ensure a one-to-one correspondence.
    warning = warnings_recorder.pop()
    text = "Reference to unknown type 'UnexposedTarget'"
    assert text in str(warning.message)


@pytest.mark.parametrize("feature", ["using", "typedef"])
# pylint: disable=redefined-outer-name
def test_target_defined_later(module_with_warnings, parent, feature):
    m, _ = module_with_warnings
    name = "{}_defined_later_target".format(feature)
    assert getattr(parent, name) is m.DefinedLaterTarget
