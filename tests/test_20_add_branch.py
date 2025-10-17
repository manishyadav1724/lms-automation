from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_add_branch(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
    page = DashboardPage(driver).go_to_v2_from_current().open_branch_settings()
    page.add_branch(
        first="John",
        last="Doe",
        name="Main Training Branch",
        email="branch.main@example.com",
        location="Texas HQ, US",
        country_text="United States",
        state_value="32",
        city="Shaktinagar",
        zip_code="23434",
    )
    assert True
