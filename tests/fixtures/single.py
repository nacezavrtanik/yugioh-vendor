
import pytest
from marketwatch import Single


@pytest.fixture()
def mrd_mirror_force():
    return Single("Mirror Force", set="MRD")


@pytest.fixture()
def dl_krebons():
    return Single("Krebons", set="DL09")
