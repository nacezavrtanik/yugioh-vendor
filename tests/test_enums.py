
import pytest
from cardmarketwatch.enums import (
    CSVField, Language, Condition, Rarity, RareColor, LanguageCode
)


def test_each_csv_field_has_exactly_one_specified_type():
    assert all([
        sum([field.is_string, field.is_integer, field.is_boolean]) == 1
        for field in CSVField
    ])


def test__csv_field_as_arg():
    assert CSVField.SET.as_arg() == "set"
    assert CSVField.FIRST_EDITION.as_arg() == "first_edition"


@pytest.mark.parametrize(("string", "enum_instance"), [
    ("english", Language.ENGLISH),
    ("fr", Language.FRENCH),
    ("deu", Language.GERMAN),
    ("m", Condition.MINT),
    ("Near Mint", Condition.NEAR_MINT),
    ("excellent", Condition.EXCELLENT),
    ("c", Rarity.COMMON),
    ("Super Rare", Rarity.SUPER_RARE),
    ("ultra rare", Rarity.ULTRA_RARE),
    ("blue", RareColor.BLUE),
    ("Green", RareColor.GREEN),
    ("-en", LanguageCode.EN),
    ("german", LanguageCode.G),
    ("f", LanguageCode.F),
])
def test_aliased_str_enum_works_for_valid_aliases(string, enum_instance):
    assert type(enum_instance)(string) is enum_instance


@pytest.mark.parametrize(("string", "enum_cls"), [
    ("spenish", Language),
    ("gud", Condition),
    ("oltra rare", Rarity),
    ("bloo", RareColor),
    ("murrican", LanguageCode)
])
def test_aliased_str_enum_instantiation_fails_for_invalid_aliases(
    string, enum_cls
):
    with pytest.raises(ValueError):
        enum_cls(string)
