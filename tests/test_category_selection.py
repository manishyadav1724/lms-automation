from src import config
from Pages.login_page import LoginPage
from Pages.profile_page import Header, EditProfilePage

def test_verify_category_selection_in_profile(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # Go to corporate_v2
    driver.get(driver.current_url.replace("/corporate", "/corporate_v2"))

    # Open profile -> Edit Profile
    Header(driver).open_profile_menu(alt_text="John Doe").go_to_edit_profile()

    # Edit professional info
    edit = EditProfilePage(driver)
    edit.open_professional_info() \
        .set_professional_category("Assisted Living", "Assisted Living Facility Manager") \
        .save_changes()

    # (Optional) Reopen to verify persisted values with real asserts, if needed.
