
import os
import platform
import contextlib

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from marketwatch import PriceBot, Binder
import marketwatch.config as cfg


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


@pytest.fixture()
def price_bot():
    return PriceBot(firefox)


@pytest.fixture()
def binder():
    return Binder.from_excel(cfg.EXCEL)
