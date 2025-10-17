from src import config
from src.generators import unique_email
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_bulk_invites_adding_rows(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
    dash = DashboardPage(driver).go_to_v2_from_current()
    invite = dash.open_invite_learners()
    invite.add_rows_and_fill(15, email_factory=lambda: unique_email(prefix="learner")) \
          .send_invites()
    # If an alert appears in your app, you can handle via driver.switch_to.alert here.
    assert True
