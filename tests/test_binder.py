
import os
import pytest
import vendor as vd
from vendor.exceptions import CSVProcessingError


def test_instatiation_succeeds_for_iterable_of_singles():
    singles = [
        vd.Single("Gemini Elf", "LON", condition=vd.Condition.LIGHT_PLAYED),
        vd.Single("Beast of Talwar", "lod", first_edition=True),
    ]
    vd.Binder(singles)
    vd.Binder(tuple(singles))
    vd.Binder(single for single in singles)


def test_instantiation_fails_for_list_of_non_singles():
    non_singles = [
        vd.Single("Ryu-Kishin", "LOB"),
        ("Aqua Madoor", "LOB"),
    ]
    with pytest.raises(TypeError):
        vd.Binder(non_singles)


def test_create_csv_template(tmpdir):
    subdir = tmpdir.mkdir("sub")
    assert os.listdir(subdir) == []
    file = subdir/"template.csv"
    vd.Binder.create_csv_template(file)
    assert os.listdir(subdir) == ["template.csv"]
    binder = vd.Binder.from_csv(file)
    assert binder[0] == vd.Single("Tatsunoko", "CORE")


def test_instantiation_from_csv_succeeds_for_all_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page\n"
        "Tatsunoko,core,english,NM,yes,,,,,,,\n"
        "Krebons,DL09,,good,,yes,,1,Rare,blue,-EN,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
        '"Brionac, Dragon of the Ice Barrier",ha01,FRA,,,,yes,,ScR,,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
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


def test_instantiation_from_csv_succeeds_for_some_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition\n"
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


def test_instantiation_from_csv_succeeds_for_redundant_fields(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page,THIS IS A REDUNDANT FIELD\n"
        "Tatsunoko,CORE,English,NM,yes,,,,,,australian,,123456789\n"
        "Krebons,DL09,,gd,,yes,,1,R,blue,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare,BLA\n"
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


def test_instantiation_from_csv_succeeds_for_empty_rows(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page\n"
        "Tatsunoko,core,english,NM,yes,,,,,,,\n"
        ",,,,,,,,,,,\n"
        "Krebons,DL09,,good,,yes,,1,Rare,blue,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
        '"Brionac, Dragon of the Ice Barrier",ha01,FRA,,,,yes,,ScR,,none,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
        ",,,,,,,,,,,\n"
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


def test_instantiation_from_csv_fails_for_missing_posargs(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page\n"
        "Tatsunoko,,English,NM,yes,,,,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(TypeError):
        vd.Binder.from_csv(file)


def test_instantiation_from_csv_fails_for_invalid_version_entry(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page\n"
        "Tatsunoko,,English,NM,yes,,,Version 2,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(CSVProcessingError):
        vd.Binder.from_csv(file)


def test_instantiation_from_csv_fails_for_invalid_boolean_entry(tmpdir):
    content = (
        "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Language Code,Article Page\n"
        "Tatsunoko,,English,NM,,,False,,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(CSVProcessingError):
        vd.Binder.from_csv(file)
