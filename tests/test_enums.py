
import pytest
import vendor as vd


def test_each_field_has_exactly_one_specified_type():
    assert all([
        sum([field.is_string, field.is_integer, field.is_boolean]) == 1
        for field in vd.Field
    ])


@pytest.mark.parametrize(("string", "enum_instance"), [
    ("english", vd.Language.ENGLISH),
    ("fr", vd.Language.FRENCH),
    ("deu", vd.Language.GERMAN),
    ("m", vd.Condition.MINT),
    ("Near Mint", vd.Condition.NEAR_MINT),
    ("excellent", vd.Condition.EXCELLENT),
    ("c", vd.Rarity.COMMON),
    ("Super Rare", vd.Rarity.SUPER_RARE),
    ("ultra rare", vd.Rarity.ULTRA_RARE),
    ("blue", vd.RareColor.BLUE),
    ("Green", vd.RareColor.GREEN),
    ("-en", vd.LanguageCode.EN),
    ("german", vd.LanguageCode.G),
    ("f", vd.LanguageCode.F),
])
def test_aliased_str_enum_works_for_valid_aliases(string, enum_instance):
    assert type(enum_instance)(string) is enum_instance


@pytest.mark.parametrize(("string", "enum_cls"), [
    ("spenish", vd.Language),
    ("gud", vd.Condition),
    ("oltra rare", vd.Rarity),
    ("bloo", vd.RareColor),
    ("murrican", vd.LanguageCode)
])
def test_aliased_str_enum_instantiation_fails_for_invalid_aliases(
    string, enum_cls
):
    with pytest.raises(ValueError):
        enum_cls(string)
