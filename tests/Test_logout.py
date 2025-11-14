from src import config
from Pages.login_page import LoginPage
from Pages.profile_page import Header

def test_logout_functionality(driver):
    # Login
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # Go to /corporate_v2
 #   driver.get(driver.current_url.replace("/corporate", "/corporate_v2"))

    # Open profile menu -> Logout
    header = Header(driver)
    header.open_profile_menu(alt_text="John Doe").logout()

    # Simple assertion: redirected to a public page with expected title or login present
    assert "login" in driver.current_url.lower() or "Online Courses and Career Opportunities" in driver.title
    driver.quit()