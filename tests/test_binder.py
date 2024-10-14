
import os
import pytest
from cardmarketwatch import Binder, Single
from cardmarketwatch.single import Language, Condition
from cardmarketwatch.binder import CSVField


def test_instatiation_succeeds_for_iterable_of_singles():
    singles = [
        Single("Gemini Elf", "LON", condition=Condition.LIGHT_PLAYED),
        Single("Beast of Talwar", "LOD", first_edition=True),
    ]
    Binder(singles)
    Binder(tuple(singles))
    Binder(single for single in singles)


def test_instantiation_fails_for_list_of_non_singles():
    non_singles = [
        Single("Ryu-Kishin", "LOB"),
        ("Aqua Madoor", "LOB"),
    ]
    with pytest.raises(TypeError):
        Binder(non_singles)


def test_create_csv_template(tmpdir):
    subdir = tmpdir.mkdir("sub")
    assert os.listdir(subdir) == []
    file = subdir/"template.csv"
    Binder.create_csv_template(file)
    assert os.listdir(subdir) == ["template.csv"]


def test_instantiation_from_csv_succeeds_for_all_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page\n"
        "Tatsunoko,CORE,English,NM,yes,,,,,,\n"
        "Krebons,DL09,,GD,,yes,,1,R,blue,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
        '"Brionac, Dragon of the Ice Barrier",HA01,French,,,,yes,,ScR,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    expected = Binder([
        Single(
            "Tatsunoko",
            "CORE",
            language="English",
            condition="NM",
            first_edition=True,
        ),
        Single(
            "Krebons",
            "DL09",
            condition=Condition.GOOD,
            signed=True,
            version=1,
            rarity="R",
            rare_color="blue",
            product_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare",
        ),
        Single(
            "Brionac, Dragon of the Ice Barrier",
            "HA01",
            language=Language.FRENCH,
            altered=True,
            rarity="ScR",
            product_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier",
        ),
    ])
    assert Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected


def test_instantiation_from_csv_succeeds_for_some_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition\n"
        "Tatsunoko,CORE,English,NM\n"
        "Krebons,DL09,,GD\n"
        '"Brionac, Dragon of the Ice Barrier",HA01,French,\n'
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    expected = Binder([
        Single(
            "Tatsunoko",
            "CORE",
            language="English",
            condition="NM",
        ),
        Single(
            "Krebons",
            "DL09",
            condition=Condition.GOOD,
        ),
        Single(
            "Brionac, Dragon of the Ice Barrier",
            "HA01",
            language=Language.FRENCH,
        ),
    ])
    assert Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected


def test_instantiation_from_csv_succeeds_for_redundant_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page,THIS IS A REDUNDANT FIELD\n"
        "Tatsunoko,CORE,English,NM,yes,,,,,,,123456789\n"
        "Krebons,DL09,,GD,,yes,,1,R,blue,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare,BLA\n"
        '"Brionac, Dragon of the Ice Barrier",HA01,French,,,,yes,,ScR,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier,\n'
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    expected = Binder([
        Single(
            "Tatsunoko",
            "CORE",
            language="English",
            condition="NM",
            first_edition=True,
        ),
        Single(
            "Krebons",
            "DL09",
            condition=Condition.GOOD,
            signed=True,
            version=1,
            rarity="R",
            rare_color="blue",
            product_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare",
        ),
        Single(
            "Brionac, Dragon of the Ice Barrier",
            "HA01",
            language=Language.FRENCH,
            altered=True,
            rarity="ScR",
            product_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier",
        ),
    ])
    assert Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected


def test_instantiation_from_csv_fails_for_missing_posargs(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page\n"
        "Tatsunoko,,English,NM,yes,,,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(TypeError):
        Binder.from_csv(file)


def test_each_csv_field_has_exactly_one_specified_type():
    assert all([
        sum([field.is_string, field.is_integer, field.is_boolean]) == 1
        for field in CSVField
    ])


def test__csv_field_as_arg():
    assert CSVField.SET.as_arg() == "set"
    assert CSVField.FIRST_EDITION.as_arg() == "first_edition"
