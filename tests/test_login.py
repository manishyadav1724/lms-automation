from src import config
from Pages.login_page import LoginPage

def test_login_and_go_v2(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
    # Navigate to /corporate_v2 from current URL
   # current = driver.current_url
   # v2 = current.replace("/corporate", "/corporate_v2")
   # driver.get(v2)
   # assert "/corporate_v2" in driver.current_url
    driver.quit()