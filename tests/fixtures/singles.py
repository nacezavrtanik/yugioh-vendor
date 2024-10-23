
import pytest
from cardmarketwatch import Single
from cardmarketwatch.single import Language


@pytest.fixture()
def mrd_mirror_force():
    return Single("Mirror Force", "MRD", version=3)


@pytest.fixture()
def dl_krebons():
    return Single("Krebons", "DL09", rare_color="green")


@pytest.fixture()
def core_tatsunoko():
    return Single(
        "Tatsunoko",
        "CORE",
        rarity="ScR",
        language=Language.ENGLISH,
        condition="NM",
        first_edition=False,
        version=None,
        altered=False,
        signed=False,
    )


@pytest.fixture()
def lob_dark_magician():
    return Single(
        "Dark Magician",
        "LOB",
        rarity="UR",
        language=Language.ENGLISH,
        condition="NM",
        first_edition=True,
        version=None,
        altered=False,
        signed=False,
    )
