import pytest
import pytypedefs as m

@pytest.mark.parametrize("parent", [None, "VisibleParent"])
@pytest.mark.parametrize("feature", ["typedef"])
def test_visibility(parent, feature):
    parent = m if parent is None else getattr(m, parent)

    for variant in ["explicitly_visible", "implicitly_visible"]:
        assert getattr(parent, "{}_{}".format(feature, variant)) is m.Target

    for variant in ["not_visible", "explicitly_hidden"]:
        assert not hasattr(parent, "{}_{}".format(feature, variant))
