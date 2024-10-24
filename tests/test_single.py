
import pytest
from cardmarketwatch import Single
from cardmarketwatch.single import Language, Condition
from cardmarketwatch.article import Article


def test_instantiation_succeeds_for_only_keyword_args():
    single = Single(
        name="Dark Magician",
        set="SDY",
        rarity="UR",
        language=Language.SPANISH,
        condition=Condition.MINT,
        first_edition=True,
    )


def test_instantiation_succeeds_for_positional_name_set_and_keyword_args():
    single = Single(
        "Dark Magician",
        "SDY",
        rarity="UR",
        language=Language.SPANISH,
        condition=Condition.MINT,
        first_edition=True,
    )


def test_instatiation_fails_for_positional_name_set_and_positional_args():
    with pytest.raises(TypeError):
        single = Single(
            "Dark Magician",
            "SDY",
            "UR",
            language=Language.ENGLISH,
            condition=Condition.MINT,
            first_edition=True,
        )


def test_instatiation_fails_for_non_string_name():
    with pytest.raises(TypeError):
        Single(["Uraby"], "LOB")


def test_instantiation_fails_for_non_string_set():
    with pytest.raises(TypeError):
        Single("Uraby", {"LOB"})


def test_instantiation_fails_for_non_string_language():
    with pytest.raises(TypeError):
        Single("Uraby", "LOB", language=12)


def test_instantiation_fails_for_invalid_language():
    with pytest.raises(ValueError):
        Single("Uraby", "LOB", language="russian")


def test_instantiation_fails_for_non_string_condition():
    with pytest.raises(TypeError):
        Single("Uraby", "LOB", condition=[])


def test_instantiation_fails_for_invalid_condition():
    with pytest.raises(ValueError):
        Single("Uraby", "LOB", condition="almost mint")


@pytest.mark.parametrize("kwargs", [
    dict(first_edition=None),
    dict(signed="no"),
    dict(altered=tuple()),
])
def test_instantiation_fails_for_non_bool_boolean_field(kwargs):
    with pytest.raises(TypeError):
        Single("uraby", "LOB", **kwargs)


def test_instantiation_fails_for_non_integer_version():
    with pytest.raises(TypeError):
        Single("uraby", "lob", version="1")


@pytest.mark.parametrize("version_number", [0, -1])
def test_instantiation_fails_for_invalid_version(version_number):
    with pytest.raises(ValueError):
        Single("uraby", "lob", version=version_number)


def test_instantiation_fails_for_non_string_rarity():
    with pytest.raises(TypeError):
        Single("uraby", "lob", rarity=False)


def test_instantiation_fails_for_invalid_rarity():
    with pytest.raises(ValueError):
        Single("uraby", "lob", rarity="super amazing mega awesome rare")


def test_instantiation_fails_for_non_string_rare_color():
    with pytest.raises(TypeError):
        Single("uraby", "lob", rare_color=[])


def test_instantiation_fails_for_invalid_rare_color():
    with pytest.raises(ValueError):
        Single("uraby", "lob", rare_color="infrared")


def test_instantiation_fails_for_non_string_article_page():
    with pytest.raises(TypeError):
        Single("uraby", "lob", article_page=False)


def test_filtered_article_page_when_article_page_is_none():
    assert Single("Sangan", "MRD").filtered_article_page is None


def test_filtered_article_page_default_filters():
    single = Single(
        "Stardust Dragon",
        "CT07",
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon?language=1&minCondition=2"
    assert single.filtered_article_page == expected


def test_filtered_article_page_some_filters_example_1():
    single = Single(
        "Sangan",
        "DB2",
        language=Language.GERMAN,
        condition="LP",
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan?language=3&minCondition=5"
    assert single.filtered_article_page == expected


def test_filtered_article_page_some_filters_example_2():
    single = Single(
        "Stardust Dragon",
        "TDGS",
        language=Language.FRENCH,
        first_edition=True,
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6?language=2&minCondition=2&isFirstEd=Y"
    assert single.filtered_article_page == expected


def test_filtered_article_page_all_filters():
    single = Single(
        "Dark Rabbit",
        "SOVR",
        language=Language.SPANISH,
        condition=Condition.EXCELLENT,
        signed=True,
        first_edition=True,
        altered=True,
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Stardust-Overdrive/Dark-Rabbit",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Stardust-Overdrive/Dark-Rabbit?language=4&minCondition=3&isSigned=Y&isFirstEd=Y&isAltered=Y"
    assert single.filtered_article_page == expected
