import pytest
import pyopaque_typedefs as m


def test_opaque_false_forces_visibility_and_sets_up_alias():
    # Target has been exposed using its own name:
    assert hasattr(m, "TargetForOpaqueFalse")

    # Typedef exists and points to target:
    assert m.typedef_opaque_false is m.TargetForOpaqueFalse


def test_opaque_false_extra_keywords_are_taken_into_account():
    assert m.typedef_opaque_false_extra_keywords is m.TargetForOpaqueFalseExtraKeywords
    instance = m.TargetForOpaqueFalseExtraKeywords()
    instance.some_dynamic_attribute = True


def test_opaque_false_target_already_exposed():
    # Extra `dynamic_attr` argument to `GENPYBIND` has no effect.
    assert m.typedef_opaque_false_already_exposed is m.TargetForOpaqueFalseAlreadyExposed
    instance = m.TargetForOpaqueFalseAlreadyExposed()
    with pytest.raises(AttributeError):
        instance.some_dynamic_attribute = True


def test_opaque_true_changes_where_the_target_is_exposed():
    # No longer exposed under it's own name
    assert not hasattr(m, "TargetForOpaque")
    instance = m.typedef_opaque()
    assert instance.x == 1

    assert not hasattr(m, "TargetForOpaqueTrue")
    instance = m.typedef_opaque_true()
    assert instance.x == 2


def test_opaque_true_extra_keywords_are_taken_into_account():
    instance = m.typedef_opaque_true_extra_keywords()
    instance.some_dynamic_attribute = True
