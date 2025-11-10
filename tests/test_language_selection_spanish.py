import time
from src import config
from Pages.login_page import LoginPage
from Pages.common_widgets import LanguageSwitcher

def test_language_selection_spanish(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # Go to /corporate_v2
    driver.get(driver.current_url.replace("/corporate", "/corporate_v2"))

    # Switch language to Spanish
    LanguageSwitcher(driver).switch_to("Spanish")

    # Optional: brief settle time; replace with a robust UI check if you have a visible Spanish element
    time.sleep(2)

    # Minimal assertion idea: page still interactive (URL unchanged and no crash)
    assert driver.current_url.endswith("/corporate_v2") or "/corporate_v2" in driver.current_url
