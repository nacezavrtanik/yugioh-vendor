
import os
import platform
import contextlib

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def system_is_ubuntu_22_04():
    if platform.system() == "Linux":
        distro_data = platform.freedesktop_os_release()
        if distro_data.get("ID") == "ubuntu" and distro_data.get("VERSION_ID") == "22.04":
            return True
    return False


@contextlib.contextmanager
def firefox_instance():
    if system_is_ubuntu_22_04():
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(executable_path="/snap/bin/geckodriver", log_output=os.devnull)
        driver = webdriver.Firefox(options=options, service=service)
    else:
        driver = webdriver.Firefox()

    driver.maximize_window()
    try:
        yield driver
    finally:
        driver.close()
