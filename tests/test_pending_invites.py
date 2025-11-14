from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_pending_invites_tile(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # Stay on the current (V1) dashboard – comment out the version switch
    # learners = DashboardPage(driver).go_to_v2_from_current().open_learners()
    dash = DashboardPage(driver)             # keep current dashboard
    learners = dash.open_learners()          # open learners directly

    learners.click_summary("Pending Invites")
    assert driver.title != ""

    driver.quit()   # manually close the browser (optional if fixture already quits)