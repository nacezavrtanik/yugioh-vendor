
import pytest
from cardmarketwatch import Binder, Single


def test_instatiation_succeeds_for_iterable_of_singles():
    singles = [
        Single("Gemini Elf", "LON", condition="LP"),
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


def test_instantiation_from_csv_succeeds(tmpdir):
    content = (
        'name,set,rarity,language,condition,first_edition,version,url,articles\n'
        'Tatsunoko,CORE,ScR,French,NM,,,,\n'
        'Krebons,TDGS,C,English,NM,,,,\n'
        '"Brionac, Dragon of the Ice Barrier",HA01,,,,,,,\n'
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    expected = Binder([
        Single("Tatsunoko", "CORE", rarity="ScR", language="French", condition="NM"),
        Single("Krebons", "TDGS", rarity="C", language="English", condition="NM"),
        Single("Brionac, Dragon of the Ice Barrier", "HA01"),

    ])
    assert Binder.from_csv(tmpdir/"sub"/"tmp.csv") == expected
