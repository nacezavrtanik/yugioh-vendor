
import pytest
from fixtures.singles import mrd_mirror_force, dl_krebons
from cardmarketwatch import Single


def test_instantiation_succeeds_for_only_keyword_args():
    single = Single(
        name="Dark Magician",
        set="SDY",
        rarity="UR",
        language="EN",
        condition="NM",
        first_edition="1st Edition",
        version="EN",
    )


def test_instantiation_succeeds_for_positional_name_set_and_keyword_args():
    single = Single(
        "Dark Magician",
        "SDY",
        rarity="UR",
        language="EN",
        condition="NM",
        first_edition="1st Edition",
        version="EN",
    )


def test_instatiation_fails_for_positional_name_set_and_positional_args():
    with pytest.raises(TypeError):
        single = Single(
            "Dark Magician",
            "SDY",
            "UR",
            language="EN",
            condition="NM",
            first_edition="1st Edition",
            version="EN",
        )


def test_filtered_url_when_url_is_none():
    assert Single("Sangan", "MRD").filtered_url is None


def test_filtered_url_default_filters():
    single = Single(
        "Stardust Dragon",
        "CT07",
        url="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon?language=1&minCondition=2"
    assert single.filtered_url == expected

def test_filtered_url_some_filters_example_1():
    single = Single(
        "Sangan",
        "DB2",
        language="German",
        condition="LP",
        url="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan?language=3&minCondition=5"
    assert single.filtered_url == expected


def test_filtered_url_some_filters_example_2():
    single = Single(
        "Stardust Dragon",
        "TDGS",
        language="French",
        first_edition=True,
        url="https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6?language=2&minCondition=2&isFirstEd=Y"
    assert single.filtered_url == expected


def test_filtered_url_all_filters():
    single = Single(
        "Dark Rabbit",
        "SOVR",
        language="Spanish",
        condition="EX",
        signed=True,
        first_edition=True,
        altered=True,
        url="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Stardust-Overdrive/Dark-Rabbit",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Stardust-Overdrive/Dark-Rabbit?language=4&minCondition=3&isSigned=Y&isFirstEd=Y&isAltered=Y"
    assert single.filtered_url == expected


def test_set_is_duelist_league_is_true(dl_krebons):
    assert dl_krebons.set_is_duelist_league


def test_set_is_duelist_league_is_false(mrd_mirror_force):
    assert not mrd_mirror_force.set_is_duelist_league


def test_set_requires_language_code_is_true(mrd_mirror_force):
    assert mrd_mirror_force.set_requires_language_code


def test_set_requires_language_code_is_false(dl_krebons):
    assert not dl_krebons.set_requires_language_code
