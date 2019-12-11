import pytest
import pytypedefs as m


@pytest.fixture(params=[None, "VisibleParent"])
def parent(request):
    return m if request.param is None else getattr(m, request.param)


@pytest.mark.parametrize("feature", ["using", "typedef"])
def test_visibility(parent, feature):
    for variant in ["explicitly_visible", "implicitly_visible"]:
        assert getattr(parent, "{}_{}".format(feature, variant)) is m.Target

    for variant in ["not_visible", "explicitly_hidden"]:
        assert not hasattr(parent, "{}_{}".format(feature, variant))


@pytest.mark.parametrize("feature", ["using", "typedef"])
def test_unexposed_target(parent, feature):
    assert not hasattr(parent, "{}_unexposed_target".format(feature))


@pytest.mark.parametrize("feature", ["using", "typedef"])
def test_target_defined_later(parent, feature):
    name = "{}_defined_later_target".format(feature)
    assert getattr(parent, name) is m.DefinedLaterTarget
