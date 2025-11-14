from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_active_learners_tile(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # learners = DashboardPage(driver).go_to_v2_from_current().open_learners()


    learners = DashboardPage(driver).open_learners()  # run directly without v2 conversion
    learners.click_summary("Active Learners")
    assert driver.title != ""
    driver.quit()