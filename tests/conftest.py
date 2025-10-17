import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src import config

@pytest.fixture(scope="session", autouse=True)
def _clean_reports():
    shutil.rmtree('reports', ignore_errors=True)

@pytest.fixture(scope="session")
def driver():
    options = FirefoxOptions()
    if config.HEADLESS:
        options.add_argument("-headless")

    drv = webdriver.Firefox(options=options)
    drv.set_page_load_timeout(config.PAGELOAD_TIMEOUT)
    yield drv
    drv.quit()
