
import pytest
import vendor as vd


@pytest.fixture()
def mrd_mirror_force():
    return vd.Single("Mirror Force", "MRD", version=3)


@pytest.fixture()
def dl_krebons():
    return vd.Single("Krebons", "DL09", rare_color="green")


@pytest.fixture()
def core_tatsunoko():
    return vd.Single(
        "Tatsunoko",
        "CORE",
        rarity="ScR",
        language=vd.Language.ENGLISH,
        condition="NM",
        first_edition=False,
        version=None,
        altered=False,
        signed=False,
    )


@pytest.fixture()
def lob_dark_magician():
    return vd.Single(
        "Dark Magician",
        "LOB",
        rarity="UR",
        language=vd.Language.ENGLISH,
        condition=vd.Condition.NEAR_MINT,
        first_edition=True,
        version=None,
        altered=False,
        signed=False,
    )
