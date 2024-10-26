
import os
import platform
import contextlib

import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

import vendor as vd


@pytest.fixture
def mrd_mirror_force():
    return vd.Single("Mirror Force", "MRD", version=3)


@pytest.fixture
def dl_krebons():
    return vd.Single("Krebons", "DL09", rare_color="green")


@pytest.fixture
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


@pytest.fixture
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


def _system_is_ubuntu_22_04_or_later():
    if platform.system() == "Linux":
        distro_data = platform.freedesktop_os_release()
        if (
            distro_data.get("ID") == "ubuntu"
            and distro_data.get("VERSION_ID") >= "22.04"
        ):
            return True
    return False


@contextlib.contextmanager
def firefox():
    if _system_is_ubuntu_22_04_or_later():
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        service = Service(
            executable_path="/snap/bin/geckodriver", log_output=os.devnull
        )
        driver = webdriver.Firefox(options=options, service=service)
    else:
        driver = webdriver.Firefox()

    driver.maximize_window()
    try:
        yield driver
    finally:
        driver.close()


@pytest.fixture
def firefox_driver():
    return firefox


@pytest.fixture
def marketwatch():
    return vd.Marketwatch(firefox)
