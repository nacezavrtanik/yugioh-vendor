
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


def test_instantiation_fails_for_non_interable():
    non_iterable = vd.Single("Mokey Mokey King", "RDS")
    with pytest.raises(TypeError):
        vd.Binder(non_iterable)


def test_instantiation_fails_for_iterable_of_non_singles():
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


def test_instantiation_from_csv_succeeds_for_some_fields(tmpdir):
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


def test_instantiation_from_csv_succeeds_for_redundant_fields(tmpdir):
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


def test_instantiation_from_csv_succeeds_for_empty_rows(tmpdir):
    content = (
        "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
        "Tatsunoko,core,english,NM,yes,,,,,,,\n"
        ",,,,,,,,,,,\n"
        "Krebons,DL09,,good,,yes,,1,Rare,blue,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
        '"Brionac, Dragon of the Ice Barrier",ha01,FRA,,,,True,,ScR,,none,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
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
        "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
        "Tatsunoko,,English,NM,yes,,,,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(TypeError):
        vd.Binder.from_csv(file)


def test_instantiation_from_csv_fails_for_invalid_version_entry(tmpdir):
    content = (
        "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
        "Tatsunoko,,English,NM,True,,,Version 2,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(CSVProcessingError):
        vd.Binder.from_csv(file)


def test_instantiation_from_csv_fails_for_invalid_boolean_entry(tmpdir):
    content = (
        "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,language_code,article_page\n"
        "Tatsunoko,,English,NM,,,nope,,,,,\n"
    )
    file = tmpdir.mkdir("sub").join("tmp.csv")
    file.write(content)

    with pytest.raises(CSVProcessingError):
        vd.Binder.from_csv(file)


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


def test_repr_eval_for_length_0():
    binder = vd.Binder([])
    from vendor import Binder
    assert eval(repr(binder)) == binder


def test_repr_eval_for_length_1():
    binder = vd.Binder([
        vd.Single("mystical space typhoon", "mrl", version=None, rarity="UR"),
    ])
    from vendor import Single, Binder
    assert eval(repr(binder)) == binder


def test_repr_eval_for_length_greater_than_or_equal_to_2_and_less_than_6():
    binder = vd.Binder([
        vd.Single("mystical space typhoon", "mrl", version=None, rarity="UR"),
        vd.Single("black pendant", "mrl", version=2, rarity=None),
        vd.Single("malevolent nuzzler", "mrl", language_code="-EN"),
    ])
    from vendor import Single, Binder
    assert eval(repr(binder)) == binder


def test_repr_eval_for_length_greater_than_or_equal_to_6():
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


@pytest.mark.skip("not yet implemented")
def test_from_dict_for_dict_of_dict():
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


@pytest.mark.skip("not yet implemented")
def test_from_dict_for_dict_of_sequence():
    assert False


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
