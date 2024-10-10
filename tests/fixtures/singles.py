
import pytest
from marketwatch import Single


@pytest.fixture()
def mrd_mirror_force():
    return Single("Mirror Force", set="MRD")


@pytest.fixture()
def dl_krebons():
    return Single("Krebons", set="DL09")


@pytest.fixture()
def core_tatsunoko():
    return Single(
        "Tatsunoko",
        set="CORE",
        rarity="ScR",
        language="EN",
        condition="NM",
        edition=None,
        version=None,
        altered=False,
        signed=False,
    )


@pytest.fixture()
def lob_dark_magician():
    return Single(
        "Dark Magician",
        set="LOB",
        rarity="UR",
        language="EN",
        condition="NM",
        edition="1st Edition",
        version=None,
        altered=False,
        signed=False,
    )


