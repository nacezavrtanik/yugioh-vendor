
import os
import pytest
from cardmarketwatch import Binder, Single
from cardmarketwatch.single import Language, Condition, Rarity, RareColor
from cardmarketwatch.binder import CSVField
from cardmarketwatch.exceptions import CSVProcessingError


def test_instatiation_succeeds_for_iterable_of_singles():
    singles = [
        Single("Gemini Elf", "LON", condition=Condition.LIGHT_PLAYED),
        Single("Beast of Talwar", "lod", first_edition=True),
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
        "Tatsunoko,core,english,NM,yes,,,,,,\n"
        "Krebons,DL09,,good,,yes,,1,Rare,blue,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
        '"Brionac, Dragon of the Ice Barrier",ha01,FRA,,,,yes,,ScR,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
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
            rarity=Rarity.RARE,
            rare_color=RareColor.BLUE,
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
        "Tatsunoko,CORE,English,near mint\n"
        "Krebons,dl09,,GD\n"
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
            language="fr",
        ),
    ])
    assert Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected


def test_instantiation_from_csv_succeeds_for_redundant_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page,THIS IS A REDUNDANT FIELD\n"
        "Tatsunoko,CORE,English,NM,yes,,,,,,,123456789\n"
        "Krebons,DL09,,gd,,yes,,1,R,blue,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare,BLA\n"
        '"Brionac, Dragon of the Ice Barrier",HA01,French,,,,yes,,scr,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier,\n'
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
            rarity=Rarity.RARE,
            rare_color=RareColor.BLUE,
            product_page="https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare",
        ),
        Single(
            "Brionac, Dragon of the Ice Barrier",
            "HA01",
            language=Language.FRENCH,
            altered=True,
            rarity="secret rare",
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


def test_instantiation_from_csv_fails_for_invalid_version_entry(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page\n"
        "Tatsunoko,,English,NM,yes,,,Version 2,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(CSVProcessingError):
        Binder.from_csv(file)


def test_instantiation_from_csv_fails_for_invalid_boolean_entry(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page\n"
        "Tatsunoko,,English,NM,,,False,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(CSVProcessingError):
        Binder.from_csv(file)
