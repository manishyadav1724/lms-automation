from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_user_can_login(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
  #  DashboardPage(driver).go_to_v2_from_current()
   # assert "/corporate_v2" in driver.current_url
    driver.quit()