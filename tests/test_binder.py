
import os
import pytest
import vendor as vd
from vendor.exceptions import (
    CSVFormatError, DictFormatError, DictProcessingError, CSVProcessingError
)


class TestInstantiation:
    @pytest.mark.parametrize("iterable", [
        list,
        tuple,
        lambda x: (y for y in x),
    ])
    def test_succeeds_for_iterable_of_singles(self, iterable):
        singles = [
            vd.Single("Gemini Elf", "LON", condition=vd.Condition.PLAYED),
            vd.Single("Beast of Talwar", "lod", first_edition=True),
        ]
        iterable_of_singles = iterable(singles)
        try:
            vd.Binder(iterable_of_singles)
        except Exception as exc_info:
            pytest.fail(f"Unexpected error: {exc_info}")

    def test_fails_for_non_interable(self):
        non_iterable = vd.Single("Mokey Mokey King", "RDS")
        with pytest.raises(TypeError) as exc_info:
            vd.Binder(non_iterable)
        expected_msg = (
            "argument 'singles' must be an iterable of 'Single' instances"
        )
        expected_notes = [
            f"Got type: Single",
            f"Got value: {non_iterable!r}",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_fails_for_iterable_of_non_singles(self):
        non_singles = [
            vd.Single("Ryu-Kishin", "LOB"),
            ("Aqua Madoor", "LOB"),
        ]
        with pytest.raises(TypeError) as exc_info:
            vd.Binder(non_singles)
        expected_msg = (
            "all items in the 'singles' iterable must be "
            "instances of type 'Single'"
        )
        expected_notes = [
            "Got item type: tuple (at index 1)",
            "Got item value: ('Aqua Madoor', 'LOB')",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes


def test_create_csv_template(tmpdir):
    subdir = tmpdir.mkdir("sub")
    assert os.listdir(subdir) == []
    file = subdir/"template.csv"
    vd.Binder.create_csv_template(file)
    assert os.listdir(subdir) == ["template.csv"]
    binder = vd.Binder.from_csv(file)
    assert binder[0] == vd.Single("Tatsunoko", "CORE")


class TestFromCSV:
    def test_csv_format_error_for_duplicate_fields(self, tmpdir):
        content = (
            "name,set,language,condition,language,REDUNDANT,name,language\n"
            "Tatsunoko,english,NM,,,,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(CSVFormatError) as exc_info:
            vd.Binder.from_csv(file)
        expected_msg = "duplicate fields: 'name', 'language'"
        expected_notes = [
            (
                "Got fields: 'name', 'set', 'language', 'condition', "
                "'language', 'REDUNDANT', 'name', 'language'"
            ),
            "Tip: Create a valid CSV with vendor.Binder.create_csv_template.",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_csv_format_error_for_missing_name_field(self, tmpdir):
        content = (
            "set,language,condition,REDUNDANT\n"
            "CORE,english,NM,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(CSVFormatError) as exc_info:
            vd.Binder.from_csv(file)
        expected_msg = "missing required fields: 'name'"
        expected_notes = [
            "Got fields: 'set', 'language', 'condition', 'REDUNDANT'",
            "Tip: Create a valid CSV with vendor.Binder.create_csv_template.",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_csv_format_error_for_missing_set_field(self, tmpdir):
        content = (
            "name,language,condition,REDUNDANT\n"
            "Tatsunoko,english,NM,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(CSVFormatError) as exc_info:
            vd.Binder.from_csv(file)
        expected_msg = "missing required fields: 'set'"
        expected_notes = [
            "Got fields: 'name', 'language', 'condition', 'REDUNDANT'",
            "Tip: Create a valid CSV with vendor.Binder.create_csv_template.",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_csv_format_error_for_missing_name_and_set_fields(self, tmpdir):
        content = (
            "language,condition,REDUNDANT\n"
            "english,NM,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(CSVFormatError) as exc_info:
            vd.Binder.from_csv(file)
        expected_msg = "missing required fields: 'name', 'set'"
        expected_notes = [
            "Got fields: 'language', 'condition', 'REDUNDANT'",
            "Tip: Create a valid CSV with vendor.Binder.create_csv_template.",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_csv_processing_error_for_invalid_integer_field_value(self, tmpdir):
        content = (
            "name,set,language,condition,REDUNDANT,version\n"
            "Tatsunoko,core,english,NM,,Version 2\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(CSVProcessingError) as exc_info:
            vd.Binder.from_csv(file)
        expected_msg = "failed to process value for field 'version'"
        expected_notes = [
            "Got type: str",
            "Got value: 'Version 2'",
            (
                "Expected type:\n"
                "  int (example: 2)\n"
                "  float, must represent an integer (example: 2.0)\n"
                "  str, must represent an integer (example: '2')"
            ),
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_succeeds_for_valid_integer_field_value(self, tmpdir):
        content = (
            "name,set,language,condition,REDUNDANT,version\n"
            "Tatsunoko,core,english,NM,,2\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        expected = vd.Binder([
            vd.Single("tatsunoko", "core", version=2)
        ])
        assert vd.Binder.from_csv(file) == expected

    def test_processing_error_for_invalid_boolean_field_value(self, tmpdir):
        content = (
            "name,set,language,condition,REDUNDANT,first_edition\n"
            "Tatsunoko,core,english,NM,,absolutely\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(CSVProcessingError) as exc_info:
            vd.Binder.from_csv(file)
        expected_msg = "failed to process value for field 'first_edition'"
        expected_notes = [
            "Got type: str",
            "Got value: 'absolutely'",
            (
                "Expected type:\n"
                "  bool (example: True)\n"
                "  str, case-insensitive, must be one of:\n"
                "    'true', 'false', 'yes', 'no' (example: 'Yes')"
            )
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    @pytest.mark.parametrize(("value", "first_edition"), [
        (True, True),    # Actual boolean
        ("true", True),  # Valid str alias
        ("YES", True),   # Valid str alias
    ])
    def test_succeeds_for_valid_boolean_field_value(
        self, tmpdir, value, first_edition
    ):
        content = (
            f"name,set,language,condition,REDUNDANT,first_edition\n"
            f"Tatsunoko,core,english,NM,,{value}\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        expected = vd.Binder([
            vd.Single("tatsunoko", "core", first_edition=first_edition)
        ])
        assert vd.Binder.from_csv(file) == expected

    def test_type_error_for_missing_name_or_set_values(self, tmpdir):
        content = (
            "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
            "Tatsunoko,,English,NM,yes,,,,,,,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(TypeError):
            vd.Binder.from_csv(file)

    def test_value_error_for_invalid_value_in_one_of_string_field(self, tmpdir):
        content = (
            "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
            "Tatsunoko,CORE,English,NOT A VALID CONDITION,True,,,2,,,,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        with pytest.raises(ValueError):
            vd.Binder.from_csv(file)

    def test_succeeds_when_all_relevant_fields_are_given(self, tmpdir):
        content = (
            "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
            "Tatsunoko,core,english,NM,true,,,,,,,\n"
            "Krebons,DL09,,good,,true,,1,Rare,blue,-EN,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
            '"Brionac, Dragon of the Ice Barrier",ha01,FRA,,,,YES,,ScR,,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        expected = vd.Binder([
            vd.Single(
                "Tatsunoko",
                "CORE",
                language="English",
                condition="NM",
                first_edition=True,
            ),
            vd.Single(
                "Krebons",
                "DL09",
                condition=vd.Condition.GOOD,
                signed=True,
                version=1,
                rarity=vd.Rarity.RARE,
                rare_color=vd.RareColor.BLUE,
                language_code=vd.LanguageCode.EN,
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare",
            ),
            vd.Single(
                "Brionac, Dragon of the Ice Barrier",
                "HA01",
                language=vd.Language.FRENCH,
                altered=True,
                rarity="ScR",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier",
            ),
        ])
        assert vd.Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected

    def test_succeeds_when_only_some_relevant_field_are_given(self, tmpdir):
        content = (
            "name,set,language,condition\n"
            "Tatsunoko,CORE,English,near mint\n"
            "Krebons,dl09,,GD\n"
            '"Brionac, Dragon of the Ice Barrier",HA01,French,\n'
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        expected = vd.Binder([
            vd.Single(
                "Tatsunoko",
                "CORE",
                language="English",
                condition="NM",
            ),
            vd.Single(
                "Krebons",
                "DL09",
                condition=vd.Condition.GOOD,
            ),
            vd.Single(
                "Brionac, Dragon of the Ice Barrier",
                "HA01",
                language="fr",
            ),
        ])
        assert vd.Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected

    def test_succeeds_when_some_redundant_fields_are_given(self, tmpdir):
        content = (
            "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page,THIS IS A REDUNDANT FIELD\n"
            "Tatsunoko,CORE,English,NM,yes,,,,,,australian,,123456789\n"
            "Krebons,DL09,,gd,,TRUE,,1,R,blue,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare,BLA\n"
            '"Brionac, Dragon of the Ice Barrier",HA01,French,,,,yes,,scr,,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier,\n'
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        expected = vd.Binder([
            vd.Single(
                "Tatsunoko",
                "CORE",
                language="English",
                condition="NM",
                first_edition=True,
                language_code="-a",
            ),
            vd.Single(
                "Krebons",
                "DL09",
                condition=vd.Condition.GOOD,
                signed=True,
                version=1,
                rarity=vd.Rarity.RARE,
                rare_color=vd.RareColor.BLUE,
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare",
            ),
            vd.Single(
                "Brionac, Dragon of the Ice Barrier",
                "HA01",
                language=vd.Language.FRENCH,
                altered=True,
                rarity="secret rare",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier",
            ),
        ])
        assert vd.Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected

    def test_succeeds_when_all_relevant_field_are_empty(self, tmpdir):
        content = (
            "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page,REDUNDANT FIELD\n"
            "Tatsunoko,core,english,NM,yes,,,,,,,,\n"
            ",,,,,,,,,,,,REDUNDANT VALUE\n"
            "Krebons,DL09,,good,,yes,,1,Rare,blue,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare,\n"
            '"Brionac, Dragon of the Ice Barrier",ha01,FRA,,,,True,,ScR,,none,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier,\n'
            ",,,,,,,,,,,,\n"
        )
        file = tmpdir.mkdir("sub").join("tmp.csv")
        file.write(content)
        expected = vd.Binder([
            vd.Single(
                "Tatsunoko",
                "CORE",
                language="English",
                condition="NM",
                first_edition=True,
            ),
            vd.Single(
                "Krebons",
                "DL09",
                condition=vd.Condition.GOOD,
                signed=True,
                version=1,
                rarity=vd.Rarity.RARE,
                rare_color=vd.RareColor.BLUE,
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare",
            ),
            vd.Single(
                "Brionac, Dragon of the Ice Barrier",
                "HA01",
                language=vd.Language.FRENCH,
                altered=True,
                rarity="ScR",
                article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier",
                language_code="american",
            ),
        ])
        assert vd.Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected


def test_to_csv(tmpdir):
    binder = vd.Binder([
        vd.Single("mezuki", "dusa", language="en", signed=True, condition="M"),
        vd.Single("gozuki", "dusa", first_edition=True, rarity="UR"),
        vd.Single("Tsukuyomi", "DUSA", language_code=vd.LanguageCode.EN),
    ])
    subdir = tmpdir.mkdir("sub")
    filename = "tmp.csv"
    binder.to_csv(subdir/filename)
    assert filename in os.listdir(subdir)
    assert vd.Binder.from_csv(subdir/filename) == binder


class TestFromDict:
    pass


class TestFromDictOfLists(TestFromDict):
    def test_dict_format_error_for_mixed_iterables(self):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "language": ["english", "french"],
            "condition": [vd.Condition.NEAR_MINT, "excellent"],
            "first_edition": [True, "yes"],
            "signed": ["no", "no"],
            "altered": ["yes", "no"],
            "version": {0: None, 1: None},
        }
        with pytest.raises(DictFormatError) as exc_info:
            vd.Binder.from_dict(binder_dict)
        expected_msg = "all dictionary values must be of the same type (supported: dict, list)"
        assert exc_info.value.args[0] == expected_msg

    def test_dict_format_error_for_inconsistent_list_lengths(self):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "language": ["english", "french"],
            "condition": [vd.Condition.NEAR_MINT, "excellent"],
            "first_edition": [True, "yes"],
            "signed": ["no", "no"],
            "altered": ["yes", "no"],
            "version": [None],
        }
        with pytest.raises(DictFormatError) as exc_info:
            vd.Binder.from_dict(binder_dict)
        expected_msg = "for a dict of lists, all lists must have equal length"
        assert exc_info.value.args[0] == expected_msg

    def test_dict_processing_error_for_invalid_string_field_value(self):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "language": [12, "french"],
        }
        with pytest.raises(DictProcessingError) as exc_info:
            vd.Binder.from_dict(binder_dict)
        expected_msg = "failed to process value for field 'language'"
        expected_notes = [
            "Got type: int",
            "Got value: 12",
            "Expected type: str",
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    def test_succeeds_for_valid_string_field_value(self):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "language": ["fr", "french"],
        }
        expected = vd.Binder([
            vd.Single("dandylion", "dusa", language=vd.Language.FRENCH),
            vd.Single("junk synchron", "dusa", language=vd.Language.FRENCH),
        ])
        assert vd.Binder.from_dict(binder_dict) == expected

    @pytest.mark.parametrize(("value", "type_str", "value_str"), [
        ([], "list", "[]"),     # Completely wrong type
        (1.1, "float", "1.1"),  # Non-integer float
        ("v1", "str", "'v1'"),  # Non-integer str
    ])
    def test_dict_processing_error_for_invalid_integer_field_value(
        self, value, type_str, value_str
    ):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "version": [2, value],
        }
        with pytest.raises(DictProcessingError) as exc_info:
            vd.Binder.from_dict(binder_dict)
        expected_msg = "failed to process value for field 'version'"
        expected_notes = [
            f"Got type: {type_str}",
            f"Got value: {value_str}",
            (
                "Expected type:\n"
                "  int (example: 2)\n"
                "  float, must represent an integer (example: 2.0)\n"
                "  str, must represent an integer (example: '2')"
            ),
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    @pytest.mark.parametrize(("value", "version"), [
        (1, 1),    # Actual integer
        (2.0, 2),  # Integer float
        ("3", 3),  # Integer str
    ])
    def test_succeeds_for_valid_integer_field_value(self, value, version):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "version": [2, value],
        }
        expected = vd.Binder([
            vd.Single("dandylion", "dusa", version=2),
            vd.Single("junk synchron", "dusa", version=version),
        ])
        assert vd.Binder.from_dict(binder_dict) == expected

    @pytest.mark.parametrize(("value", "type_str", "value_str"), [
        (1, "int", "1"),            # Completely wrong type
        ("nope", "str", "'nope'"),  # Invalid str alias
    ])
    def test_dict_processing_error_for_invalid_boolean_field_value(
        self, value, type_str, value_str
    ):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "signed": [True, value],
        }
        with pytest.raises(DictProcessingError) as exc_info:
            vd.Binder.from_dict(binder_dict)
        expected_msg = "failed to process value for field 'signed'"
        expected_notes = [
            f"Got type: {type_str}",
            f"Got value: {value_str}",
            (
                "Expected type:\n"
                "  bool (example: True)\n"
                "  str, case-insensitive, must be one of:\n"
                "    'true', 'false', 'yes', 'no' (example: 'Yes')"
            ),
        ]
        assert exc_info.value.args[0] == expected_msg
        assert exc_info.value.__notes__ == expected_notes

    @pytest.mark.parametrize(("value", "altered"), [
        (False, False),    # Actual boolean
        ("false", False),  # Valid str alias
        ("No", False),     # Valid str alias (capitalized)
    ])
    def test_succeeds_for_valid_boolean_field_value(self, value, altered):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "altered": [True, value],
        }
        expected = vd.Binder([
            vd.Single("dandylion", "dusa", altered=True),
            vd.Single("junk synchron", "dusa", altered=altered),
        ])
        assert vd.Binder.from_dict(binder_dict) == expected

    def test_type_error_for_missing_name_or_set_values(self):
        binder_dict = {
            "name": ["Dandylion", None],
            "set": ["DUSA", "dusa"],
        }
        with pytest.raises(TypeError):
            vd.Binder.from_dict(binder_dict)

    def test_value_error_for_invalid_value_in_one_of_string_field(self):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "condition": ["gem mint", "NM"],
        }
        with pytest.raises(ValueError):
            vd.Binder.from_dict(binder_dict)

    def test_succeeds_for_valid_input(self):
        binder_dict = {
            "name": ["Dandylion", "junk synchron"],
            "set": ["DUSA", "dusa"],
            "language": [vd.Language.SPANISH, "french"],
            "condition": [vd.Condition.NEAR_MINT, "excellent"],
            "first_edition": [True, "yes"],
            "signed": ["no", "no"],
            "altered": ["yes", "no"],
            "version": [None, None],
            "rarity": [vd.Rarity.ULTRA_RARE, "UR"],
            # "rare_color": some fields may be left unspecified
            "language_code": [None, None],
            "article_page": [
                "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-Saga/Dandylion",
                None,
            ],
        }
        expected = vd.Binder([
           vd.Single(
               "dandylion",
               "dusa",
               language="spanish",
               condition="near mint",
               first_edition=True,
               altered=True,
               rarity="UR",
               article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-Saga/Dandylion",
            ),
            vd.Single(
                "Junk Synchron",
                "Dusa",
                language=vd.Language.FRENCH,
                condition=vd.Condition.EXCELLENT,
                first_edition=True,
                rarity=vd.Rarity.ULTRA_RARE,
            )
        ])
        assert vd.Binder.from_dict(binder_dict) == expected


@pytest.mark.skip("not yet implemented")
class TestFromDictOfDicts(TestFromDict):
    def test_dict_format_error_for_mixed_iterables(self):
        binder_dict = {
            "name": {0: "Dandylion", 1: "junk synchron"},
            "set": {0: "DUSA", 1: "dusa"},
            "language": {0: vd.Language.SPANISH, 1: "french"},
            "condition": {1: "excellent"},
            "first_edition": {0: True, 1: "yes"},
            "signed": {},
            "altered": {0: "yes"},
            "version": [],
        }
        with pytest.raises(DictFormatError) as exc_info:
            vd.Binder.from_dict(binder_dict)
        expected_msg = "all dictionary values must be of the same type (supported: dict, list)"
        assert exc_info.value.args[0] == expected_msg

    def test_succeeds_for_valid_input(self):
        binder_dict = {
            "name": {0: "Dandylion", 1: "junk synchron"},
            "set": {0: "DUSA", 1: "dusa"},
            "language": {0: vd.Language.SPANISH, 1: "french"},
            "condition": {1: "excellent"},
            "first_edition": {0: True, 1: "yes"},
            "signed": {},
            "altered": {0: "yes"},
            "version": {},
            "rarity": {0: vd.Rarity.ULTRA_RARE, 1: "UR"},
            # "rare_color": {},  # Some fields may be left unspecified
            "language_code": {},
            "article_page": {
                0: "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-Saga/Dandylion",
                1: None,
            },
        }
        expected = vd.Binder([
           vd.Single(
               "dandylion",
               "dusa",
               language="spanish",
               condition="near mint",
               first_edition=True,
               altered=True,
               rarity="UR",
               article_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-Saga/Dandylion",
            ),
            vd.Single(
                "Junk Synchron",
                "Dusa",
                language=vd.Language.FRENCH,
                condition=vd.Condition.EXCELLENT,
                first_edition=True,
                rarity=vd.Rarity.ULTRA_RARE,
            )
        ])
        assert vd.Binder.from_dict(binder_dict) == expected


def test_to_dict():
    binder = vd.Binder([
        vd.Single("mezuki", "dusa", language="en", signed=True, condition="M"),
        vd.Single("gozuki", "dusa", first_edition=True, rarity="UR"),
        vd.Single("Tsukuyomi", "DUSA", language_code=vd.LanguageCode.EN),
    ])
    expected = {
        "name": {0: "Mezuki", 1: "Gozuki", 2: "Tsukuyomi"},
        "set": {0: "DUSA", 1: "DUSA", 2: "DUSA"},
        "language": {
            0: vd.Language.ENGLISH,
            1: vd.Language.ENGLISH,
            2: vd.Language.ENGLISH,
        },
        "condition": {
            0: vd.Condition.MINT,
            1: vd.Condition.NEAR_MINT,
            2: vd.Condition.NEAR_MINT,
        },
        "first_edition": {0: False, 1: True, 2: False},
        "signed": {0: True, 1: False, 2: False},
        "altered": {0: False, 1: False, 2: False},
        "version": {0: None, 1: None, 2: None},
        "rarity": {0: None, 1: vd.Rarity.ULTRA_RARE, 2: None},
        "rare_color": {0: None, 1: None, 2: None},
        "language_code": {0: None, 1: None, 2: vd.LanguageCode.EN},
        "article_page": {0: None, 1: None, 2: None},
    }
    assert binder.to_dict() == expected


class TestReprEval:
    # The tests in this class require importing the Binder class without the
    # package namespace prefix.

    def test_for_length_0(self):
        binder = vd.Binder([])
        from vendor import Binder
        assert eval(repr(binder)) == binder


    def test_for_length_1(self):
        binder = vd.Binder([
            vd.Single("mystical space typhoon", "mrl", version=None, rarity="UR"),
        ])
        from vendor import Single, Binder
        assert eval(repr(binder)) == binder


    def test_for_length_greater_than_or_equal_to_2_and_less_than_6(self):
        binder = vd.Binder([
            vd.Single("mystical space typhoon", "mrl", version=None, rarity="UR"),
            vd.Single("black pendant", "mrl", version=2, rarity=None),
            vd.Single("malevolent nuzzler", "mrl", language_code="-EN"),
        ])
        from vendor import Single, Binder
        assert eval(repr(binder)) == binder


    def test_for_length_greater_than_or_equal_to_6(self):
        binder = vd.Binder([
            vd.Single("mystical space typhoon", "mrl", version=None, rarity="UR"),
            vd.Single("black pendant", "mrl", version=2, rarity=None),
            vd.Single("malevolent nuzzler", "mrl", language_code="-EN"),
            vd.Single("mystical space typhoon", "mrl", version=None, rarity="UR"),
            vd.Single("black pendant", "mrl", version=2, rarity=None),
            vd.Single("malevolent nuzzler", "mrl", language_code="-EN"),
        ])
        from vendor import Single, Binder
        assert eval(repr(binder)) != binder
        assert eval(repr(binder)) == binder[:2] + binder[-2:]


def test_addition():
    mystic_tomato = vd.Single("Mystic Tomato", "MRL")
    mother_grizzly = vd.Single("Mother Grizzly", "MRL")
    shining_angel = vd.Single("Shining Angel", "MRL")
    binder_1 = vd.Binder([mystic_tomato])
    binder_2 = vd.Binder([mother_grizzly, shining_angel])
    binder_sum = vd.Binder([mystic_tomato, mother_grizzly, shining_angel])
    assert binder_1 + binder_2 == binder_sum


def test_mutable_sequence_operations():
    ojama_black = vd.Single("ojama black", "IOC")
    ojama_green = vd.Single("ojama green", "IOC")
    ojama_yellow = vd.Single("ojama yellow", "IOC")

    binder = vd.Binder([ojama_black, ojama_green])
    assert ojama_green in binder

    binder.append(ojama_yellow)
    assert binder[-1] == ojama_yellow
    assert binder.pop() == ojama_yellow

    binder_2 = vd.Binder([ojama_yellow])
    binder_2.extend(binder)
    assert len(binder_2) == 3

    del binder_2[1]
    assert binder_2 == vd.Binder([ojama_yellow, ojama_green])

    binder_2.reverse()
    assert  binder_2 == vd.Binder([ojama_green, ojama_yellow])

    binder_2.clear()
    assert len(binder_2) == 0


@pytest.mark.skip("not yet implemented")
def test_pandas_dataframe_from_binder():
    binder = vd.Binder([
        vd.Single(
            "flame swordsman", "mrl", first_edition=True, version=2, rarity="C"
        ),
        vd.Single(
            "hungry burger", "srl", condition=vd.Condition.LIGHT_PLAYED
        ),
    ])
    binder_df = pd.DataFrame(single.to_dict() for single in binder)
