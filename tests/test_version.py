
import pytest
from cardmarketwatch.descriptors import Version
from fixtures.singles import dl_krebons, mrd_mirror_force


def test_instantiation_succeeds_with_integer_value():
    class C:
        version = Version
        set = "MRL"
        def __init__(self, version):
            self.version = version
    instance = C(3)
    assert instance.version == 3


def test_instantiation_succeeds_with_none_as_default_value():
    class C:
        version = Version()
        set = "LOB"
    instance = C()
    assert instance.version is None


def test_instantiation_fails_with_non_integer_non_none_value():
    class C:
        version = Version()
        set = "MRL"
        def __init__(self, version):
            self.version = version
    with pytest.raises(TypeError):
        C("123")


def test_assignment_succeeds_for_int_and_none():
    class C:
        version = Version()
        set = "MRD"
    instance = C()
    instance.version = 1
    assert instance.version == 1
    instance.version = None
    assert instance.version is None


def test_assignment_fails_for_non_int():
    class C:
        version = Version()
    instance = C()
    with pytest.raises(TypeError):
        instance.version = "1"


@pytest.mark.parametrize("version_number", [0, -1])
def test_assignment_fails_for_non_positive_int(version_number):
    class C:
        version = Version()
    instance = C()
    with pytest.raises(ValueError):
        instance.version = version_number


def test_set_is_duelist_league_is_true(dl_krebons):
    version = Version()
    assert version._set_is_duelist_league(dl_krebons) is True


def test_set_is_duelist_league_is_false(mrd_mirror_force):
    version = Version()
    assert version._set_is_duelist_league(mrd_mirror_force) is False


def test_set_requires_language_code_is_true(mrd_mirror_force):
    version = Version()
    assert version._set_requires_language_code(mrd_mirror_force) is True


def test_set_requires_language_code_is_false(dl_krebons):
    version = Version()
    assert version._set_requires_language_code(dl_krebons) is False
