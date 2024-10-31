
import dataclasses
import pytest
import vendor as vd


class TestInstantiation:
    def test_succeeds_for_enums(self):
        try:
            vd.Single(
                "Dark Magician",
                "SDY",
                language=vd.Language.GERMAN,
                condition=vd.Condition.MINT,
                first_edition=True,
                signed=False,
                altered=False,
                version=1,
                rarity=vd.Rarity.ULTRA_RARE,
                rare_color=None,
                language_code=vd.LanguageCode.G,
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Starter-Deck-Yugi/Dark-Magician-V1-Ultra-Rare",
            )
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_succeeds_for_exact_matches_to_enum_values(self):
        try:
            vd.Single(
                "Dark Magician",
                "SDY",
                language="German",
                condition="Mint",
                first_edition=True,
                signed=False,
                altered=False,
                version=1,
                rarity="Ultra Rare",
                rare_color=None,
                language_code="-G",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Starter-Deck-Yugi/Dark-Magician-V1-Ultra-Rare",
            )
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_succeeds_for_enum_aliases(self):
        try:
            vd.Single(
                "Dark Magician",
                "SDY",
                language="deu",
                condition="m",
                first_edition=True,
                signed=False,
                altered=False,
                version=1,
                rarity="UR",
                rare_color=None,
                language_code="german",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Starter-Deck-Yugi/Dark-Magician-V1-Ultra-Rare",
            )
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_succeeds_for_positional_name_and_set_and_keyword_args(self):
        try:
            single = vd.Single(
                "Blue-Eyes White Dragon",
                "SDK",
                language="english",
                condition="light played",
                first_edition=True,
                signed=True,
                altered=False,
                version=3,
                rarity="ultra rare",
                rare_color=None,
                language_code="-a",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Starter-Deck-Kaiba/Blue-Eyes-White-Dragon-V3-Ultra-Rare",
            )
        except Exception as exc_info:
            pytest.fail(f"Unexpected exception: {exc_info}")

    def test_succeeds_for_all_args_passed_as_keyword_args(self):
        try:
            single = vd.Single(
                name="Blue-Eyes White Dragon",
                set="SDK",
                language="english",
                condition="light played",
                first_edition=True,
                signed=True,
                altered=False,
                version=3,
                rarity="ultra rare",
                rare_color=None,
                language_code="-a",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Starter-Deck-Kaiba/Blue-Eyes-White-Dragon-V3-Ultra-Rare",
            )
        except Exception as exc_info:
            pytest.fail(f"Unexpected exception: {exc_info}")

    def test_fails_for_positional_args_other_than_name_and_set(self):
        with pytest.raises(TypeError):
            vd.Single(
                "Blue-Eyes White Dragon",
                "SDK",
                "english",       # passed as positional arg
                "light played",  # passed as positional arg
                True,            # passed as positional arg
                signed=True,
                altered=False,
                version=3,
                rarity="ultra rare",
                rare_color=None,
                language_code="-a",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Starter-Deck-Kaiba/Blue-Eyes-White-Dragon-V3-Ultra-Rare",
            )

    def test_fails_for_missing_positional_args(self):
        with pytest.raises(TypeError):
            vd.Single("Blue-Eyes White Dragon")

    def test_succeeds_for_missing_keyword_args(self):
        try:
            vd.Single("Blue-Eyes White Dragon", "SDK", language="english")
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")


class TestInstantiationErrors:
    def test_type_error_for_non_string_name(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single(["Uraby"], "LOB")
        expected_msg = (
            "attribute 'name' must be of type 'str', "
            "got type 'list' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_name_none(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single(None, "LOB")
        expected_msg = (
            "attribute 'name' must be of type 'str', "
            "got type 'NoneType' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_string_set(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", ("LOB",))
        expected_msg = (
            "attribute 'set' must be of type 'str', "
            "got type 'tuple' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_set_none(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", None)
        expected_msg = (
            "attribute 'set' must be of type 'str', "
            "got type 'NoneType' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_string_language(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", language=12)
        expected_msg = (
            "attribute 'language' must be of type 'str', "
            "got type 'int' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_language_none(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", language=None)
        expected_msg = (
            "attribute 'language' must be of type 'str', "
            "got type 'NoneType' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_value_error_for_invalid_language(self):
        with pytest.raises(ValueError) as exc_info:
            vd.Single("Uraby", "LOB", language="russian")
        expected_msg = "'russian' is not a valid Language"
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_string_condition(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", condition=False)
        expected_msg = (
            "attribute 'condition' must be of type 'str', "
            "got type 'bool' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_condition_none(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", condition=None)
        expected_msg = (
            "attribute 'condition' must be of type 'str', "
            "got type 'NoneType' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_value_error_for_invalid_condition(self):
        with pytest.raises(ValueError) as exc_info:
            vd.Single("Uraby", "LOB", condition="almost mint")
        expected_msg = "'almost mint' is not a valid Condition"
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_boolean_first_edition(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", first_edition="true")
        expected_msg = (
            "attribute 'first_edition' must be of type 'bool', "
            "got type 'str' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_boolean_signed(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", signed=0)
        expected_msg = (
            "attribute 'signed' must be of type 'bool', "
            "got type 'int' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_boolean_altered(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("Uraby", "LOB", altered=None)
        expected_msg = (
            "attribute 'altered' must be of type 'bool', "
            "got type 'NoneType' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_integer_version(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("uraby", "lob", version="1")
        expected_msg = (
            "attribute 'version' must be of type 'int', or None, "
            "got type 'str' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_no_error_for_version_none(self):
        try:
            vd.Single("Uraby", "LOB", version=None)
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_type_error_for_non_string_rarity(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("uraby", "lob", rarity=False)
        expected_msg = (
            "attribute 'rarity' must be of type 'str', or None, "
            "got type 'bool' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_no_error_for_rarity_none(self):
        try:
            vd.Single("Uraby", "LOB", rarity=None)
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_value_error_for_invalid_rarity(self):
        with pytest.raises(ValueError) as exc_info:
            vd.Single("uraby", "lob", rarity="super amazing mega awesome rare")
        expected_msg = (
            "'super amazing mega awesome rare' is not a valid Rarity"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_string_rare_color(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("uraby", "lob", rare_color=[])
        expected_msg = (
            "attribute 'rare_color' must be of type 'str', or None, "
            "got type 'list' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_no_error_for_rare_color_none(self):
        try:
            vd.Single("Uraby", "LOB", rare_color=None)
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_value_error_for_invalid_rare_color(self):
        with pytest.raises(ValueError) as exc_info:
            vd.Single("uraby", "lob", rare_color="infrared")
        expected_msg = "'infrared' is not a valid RareColor"
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_string_language_code(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("uraby", "lob", language_code=False)
        expected_msg = (
            "attribute 'language_code' must be of type 'str', or None, "
            "got type 'bool' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_no_error_for_language_code_none(self):
        try:
            vd.Single("Uraby", "LOB", language_code=None)
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_value_error_for_invalid_language_code(self):
        with pytest.raises(ValueError) as exc_info:
            vd.Single("uraby", "lob", language_code="-S")
        expected_msg = "'-S' is not a valid LanguageCode"
        assert exc_info.value.args[0] == expected_msg

    def test_type_error_for_non_string_article_page(self):
        with pytest.raises(TypeError) as exc_info:
            vd.Single("uraby", "lob", article_page=False)
        expected_msg = (
            "attribute 'article_page' must be of type 'str', or None, "
            "got type 'bool' instead"
        )
        assert exc_info.value.args[0] == expected_msg

    def test_no_error_for_article_page_none(self):
        try:
            vd.Single("Uraby", "LOB", article_page=None)
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")


@pytest.mark.parametrize(("attr", "value"), [
    ("name", "Snatcher of Shapes"),
    ("set", "LOB"),
    ("language", "english"),
    ("condition", vd.Condition.MINT),
    ("first_edition", False),
    ("signed", True),
    ("altered", False),
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


def test_repr_evaluation():
    single = vd.Single(
        "dark armed dragon",
        "ptdn",
        language=vd.Language.SPANISH,
        condition="ex",
        first_edition=False,
        signed=True,
        altered=False,
        version=None,
        rarity=vd.Rarity.SECRET_RARE,
        rare_color=None,
        language_code=None,
        article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Phantom-Darkness/Dark-Armed-Dragon",
    )
    # Requires import without package namespace prefix
    from vendor import Single
    assert eval(repr(single)) == single


def test_str():
    single = vd.Single("judgement dragon", "lodt")
    expected = "Judgement Dragon (LODT)"
    assert str(single) == expected


def test_as_dict():
    single = vd.Single(
        "rabidragon", "phsw", language=vd.Language.PORTUGUESE, condition="PO"
    )
    expected = dict(
        name="Rabidragon",
        set="PHSW",
        language=vd.Language.PORTUGUESE,
        condition=vd.Condition.POOR,
        first_edition=False,
        altered=False,
        signed=False,
        version=None,
        rarity=None,
        rare_color=None,
        language_code=None,
        article_page=None,
    )
    assert single.to_dict() == expected


class TestFilteredArticlePage:
    def test_is_none_when_article_page_is_none(self):
        assert vd.Single("Sangan", "MRD").filtered_article_page is None

    def test_for_default_attribute_values(self):
        single = vd.Single(
            "Stardust Dragon",
            "CT07",
            article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon",
        )
        expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Collectors-Tins-2010/Stardust-Dragon?language=1&minCondition=2"
        assert single.filtered_article_page == expected

    def test_for_some_non_default_attribute_values_1(self):
        single = vd.Single(
            "Sangan",
            "DB2",
            language=vd.Language.GERMAN,
            condition="LP",
            article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan",
        )
        expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Dark-Beginning-2/Sangan?language=3&minCondition=5"
        assert single.filtered_article_page == expected

    def test_for_some_non_default_attribute_values_2(self):
        single = vd.Single(
            "Stardust Dragon",
            "TDGS",
            language=vd.Language.FRENCH,
            first_edition=True,
            article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6",
        )
        expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/The-Duelist-Genesis/Stardust-Dragon-V-6?language=2&minCondition=2&isFirstEd=Y"
        assert single.filtered_article_page == expected

    def test_for_when_all_relevant_attribute_values_are_non_default(self):
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
