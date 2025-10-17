from src import config
from Pages.registration_page import RegistrationPage

def test_registration_flow(driver):
    reg = RegistrationPage(driver)
    reg.start_from_home(config.BASE_URL) \
       .go_to_group_discount() \
       .start_registration(company="AHCA", email=config.REG_EMAIL) \
       .fill_basic_info_and_continue(first="John", last="Doe", mobile="9876543210", password="Test1@1234") \
       .accept_terms_and_submit() \
       .pick_category_and_save(category_value="523", subcategory_value="1850") \
       .switch_language_to_spanish() \
       .logout_via_profile()

    assert driver.title == "Online Courses and Career Opportunities"
