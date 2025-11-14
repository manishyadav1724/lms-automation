# tests/test_registration.py
'''import time, random
from src import config
from Pages.registration_page import RegistrationPage

def unique_email(domain: str = "cpraedcourse.com", prefix: str = "reguser"):
    """Generate a unique email each run."""
    return f"{prefix}{int(time.time())}{random.randint(1000,9999)}@{domain}"

def test_registration_flow(driver):
    # auto-generated unique email
    email = unique_email()

    reg = RegistrationPage(driver)
    reg.start_from_home(config.BASE_URL)
    reg.go_to_group_discount()
    reg.start_registration(company="AHCA", email=email)
    reg.fill_basic_info_and_continue(
        first="John",
        last="Doe",
        mobile="9876543210",
        password="Test1@1234"
    )

    time.sleep(1)  # short wait before clicking the checkbox/submit
    reg.pick_category_and_save(category_value="523", subcategory_value="1850")
    reg.accept_terms_and_submit()
    #reg.pick_category_and_save(category_value="523", subcategory_value="1850")

    # removed:
    # reg.switch_language_to_spanish()
    # reg.logout_via_profile()

    assert driver.title == "Online Courses and Career Opportunities" '''

# tests/test_registration.py
import time, random
from src import config
from Pages.registration_page import RegistrationPage

def unique_email(domain: str = "cpraedcourse.com", prefix: str = "reguser"):
    return f"{prefix}{int(time.time())}{random.randint(1000,9999)}@{domain}"

def test_registration_flow(driver):
    email = unique_email()

    reg = RegistrationPage(driver)
    (reg.start_from_home(config.BASE_URL)
       .go_to_group_discount()
       .start_registration(company="AHCA", email=email)
       .fill_basic_info_and_continue(first="John", last="Doe",
                                     mobile="9876543210", password="Test1@1234")
       # 1) Choose category/sub-category and Save
       .pick_category_and_save(category_value="523", subcategory_value="1850")
       # 2) Accept terms and Submit (final)
       .accept_terms_and_submit())

    # Remove the unconditional v2 jump. Only keep if you *must*:
    driver.get(driver.current_url.replace("/corporate", "/corporate_v2"))
    driver.quit()




