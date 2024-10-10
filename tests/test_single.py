
import pytest
from fixtures.single import mrd_mirror_force, dl_krebons
from marketwatch import Single


def test_instantiation_succeeds_for_only_keyword_args():
    single = Single(
        name="Dark Magician",
        set="SDY",
        rarity="UR",
        language="EN",
        condition="NM",
        edition="1st Edition",
        version="EN",
    )


def test_instantiation_succeeds_for_positional_name_and_keyword_args():
    single = Single(
        "Dark Magician",
        set="SDY",
        rarity="UR",
        language="EN",
        condition="NM",
        edition="1st Edition",
        version="EN",
    )


def test_instatiation_fails_for_positional_name_and_positional_args():
    with pytest.raises(TypeError):
        single = Single(
            "Dark Magician",
            "SDY",
            rarity="UR",
            language="EN",
            condition="NM",
            edition="1st Edition",
            version="EN",
        )


def test_set_is_duelist_league_is_true(dl_krebons):
    assert dl_krebons.set_is_duelist_league


def test_set_is_duelist_league_is_false(mrd_mirror_force):
    assert not mrd_mirror_force.set_is_duelist_league


def test_set_requires_language_code_is_true(mrd_mirror_force):
    assert mrd_mirror_force.set_requires_language_code


def test_set_requires_language_code_is_false(dl_krebons):
    assert not dl_krebons.set_requires_language_code
