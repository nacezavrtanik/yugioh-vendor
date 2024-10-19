
import pytest
from cardmarketwatch.version import Version


def test_instantiation_succeeds_with_none_as_default_value():
    class C:
        version = Version()
        set_is_duelist_league = None
    instance = C()
    assert instance.version is None


def test_assignment_succeeds_for_int_and_none():
    class C:
        version = Version()
        set_is_duelist_league = None
    instance = C()
    instance.version = 1
    assert instance.version == 1
    instance.version = None
    assert instance.version is None


def test_assignment_fails_for_non_int():
    class C:
        version = Version()
        set_is_duelist_league = None
    instance = C()
    with pytest.raises(TypeError):
        instance.version = "1"


@pytest.mark.parametrize("version_number", [0, -1])
def test_assignment_fails_for_non_positive_int(version_number):
    class C:
        version = Version()
        set_is_duelist_league = None
    instance = C()
    with pytest.raises(ValueError):
        instance.version = version_number
