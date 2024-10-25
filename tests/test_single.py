
import dataclasses
import pytest
import vendor as vd


def test_instantiation_succeeds_for_only_keyword_args():
    single = vd.Single(
        name="Dark Magician",
        set="SDY",
        rarity="UR",
        language=vd.Language.SPANISH,
        condition=vd.Condition.MINT,
        first_edition=True,
        language_code="E",
    )


def test_instantiation_succeeds_for_positional_name_set_and_keyword_args():
    single = vd.Single(
        "Dark Magician",
        "SDY",
        rarity="UR",
        language=vd.Language.SPANISH,
        condition=vd.Condition.MINT,
        first_edition=True,
        language_code=vd.LanguageCode.E,
    )


def test_instatiation_fails_for_positional_name_set_and_positional_args():
    with pytest.raises(TypeError):
        single = vd.Single(
            "Dark Magician",
            "SDY",
            "UR",
            language=vd.Language.ENGLISH,
            condition=vd.Condition.MINT,
            first_edition=True,
        )


def test_instatiation_fails_for_non_string_name():
    with pytest.raises(TypeError):
        vd.Single(["Uraby"], "LOB")


def test_instantiation_fails_for_non_string_set():
    with pytest.raises(TypeError):
        vd.Single("Uraby", {"LOB"})


def test_instantiation_fails_for_non_string_language():
    with pytest.raises(TypeError):
        vd.Single("Uraby", "LOB", language=12)


def test_instantiation_fails_for_invalid_language():
    with pytest.raises(ValueError):
        vd.Single("Uraby", "LOB", language="russian")


def test_instantiation_fails_for_non_string_condition():
    with pytest.raises(TypeError):
        vd.Single("Uraby", "LOB", condition=[])


def test_instantiation_fails_for_invalid_condition():
    with pytest.raises(ValueError):
        vd.Single("Uraby", "LOB", condition="almost mint")


@pytest.mark.parametrize("kwargs", [
    dict(first_edition=None),
    dict(signed="no"),
    dict(altered=tuple()),
])
def test_instantiation_fails_for_non_bool_boolean_field(kwargs):
    with pytest.raises(TypeError):
        vd.Single("uraby", "LOB", **kwargs)


def test_instantiation_fails_for_non_integer_version():
    with pytest.raises(TypeError):
        vd.Single("uraby", "lob", version="1")


@pytest.mark.parametrize("version_number", [0, -1])
def test_instantiation_fails_for_invalid_version(version_number):
    with pytest.raises(ValueError):
        vd.Single("uraby", "lob", version=version_number)


def test_instantiation_fails_for_non_string_rarity():
    with pytest.raises(TypeError):
        vd.Single("uraby", "lob", rarity=False)


def test_instantiation_fails_for_invalid_rarity():
    with pytest.raises(ValueError):
        vd.Single("uraby", "lob", rarity="super amazing mega awesome rare")


def test_instantiation_fails_for_non_string_rare_color():
    with pytest.raises(TypeError):
        vd.Single("uraby", "lob", rare_color=[])


def test_instantiation_fails_for_invalid_rare_color():
    with pytest.raises(ValueError):
        vd.Single("uraby", "lob", rare_color="infrared")


def test_instantiation_fails_for_non_string_article_page():
    with pytest.raises(TypeError):
        vd.Single("uraby", "lob", article_page=False)


@pytest.mark.parametrize(("attr", "value"), [
    ("name", "Snatcher of Shapes"),
    ("set", "LOB"),
    ("language", "english"),
    ("condition", vd.Condition.MINT),
    ("first_edition", False),
    ("version", 2),
    ("rarity", vd.Rarity.GHOST_RARE),
    ("rare_color", "green"),
    ("language_code", "-en"),
    ("article_page", "https://www.example.com"),
])
def test_instances_are_immutable(attr, value):
    single = vd.Single(
        name="Shapesnatch",
        set="PGD",
        language=vd.Language.SPANISH,
        condition=vd.Condition.POOR,
        first_edition=True,
        version=None,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(single, attr, value)


def test_equality():
    single_1 = vd.Single(
        "Souleater",
        "PGD",
        language=vd.Language.ENGLISH,
        condition=vd.Condition.NEAR_MINT,
        first_edition=True,
    )
    single_2 = vd.Single(
        "souleater",
        "pgd",
        language="eng",
        condition="nm",
        first_edition=True,
    )
    assert single_1 == single_2


def test_filtered_article_page_when_article_page_is_none():
    assert vd.Single("Sangan", "MRD").filtered_article_page is None


def test_filtered_article_page_default_filters():
    single = vd.Single(
        "Stardust Dragon",
        "CT07",
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon?language=1&minCondition=2"
    assert single.filtered_article_page == expected


def test_filtered_article_page_some_filters_example_1():
    single = vd.Single(
        "Sangan",
        "DB2",
        language=vd.Language.GERMAN,
        condition="LP",
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan?language=3&minCondition=5"
    assert single.filtered_article_page == expected


def test_filtered_article_page_some_filters_example_2():
    single = vd.Single(
        "Stardust Dragon",
        "TDGS",
        language=vd.Language.FRENCH,
        first_edition=True,
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6?language=2&minCondition=2&isFirstEd=Y"
    assert single.filtered_article_page == expected


def test_filtered_article_page_all_filters():
    single = vd.Single(
        "Dark Rabbit",
        "SOVR",
        language=vd.Language.SPANISH,
        condition=vd.Condition.EXCELLENT,
        signed=True,
        first_edition=True,
        altered=True,
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Stardust-Overdrive/Dark-Rabbit",
    )
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Stardust-Overdrive/Dark-Rabbit?language=4&minCondition=3&isSigned=Y&isFirstEd=Y&isAltered=Y"
    assert single.filtered_article_page == expected
