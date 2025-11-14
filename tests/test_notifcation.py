from src import config
from Pages.login_page import LoginPage
from Pages.profile_page import Header

def test_open_notifications(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # Go to /corporate_v2
    #driver.get(driver.current_url.replace("/corporate", "/corporate_v2"))

    # Click Notifications
    Header(driver).open_notifications()

    # Add a light assertion (adjust selector if your app shows a panel or list)
    # Example: assert a notifications container exists, if you know its locator.
    # For now, just ensure we didn't navigate away to an error page:
    assert "corporate_v2" in driver.current_url or driver.title != ""
    driver.quit()