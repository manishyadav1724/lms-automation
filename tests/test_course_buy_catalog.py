'''from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_course_buy_from_catalog(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
    dash = DashboardPage(driver).go_to_v2_from_current()

    checkout = (dash.open_course_catalog()
                    .search_course("Suicide Prevention and Screening")
                    .add_first_result_to_cart()
                    .proceed_to_checkout())

    checkout.fill_cardholder("Manish Yadav") \
            .fill_card_number("4242424242424242") \
            .fill_expiry("12/32") \
            .fill_cvc("895") \
            .choose_country("United States") \
            .fill_postal("11230") \
            .apply_promo("seg10") \
            .place_order()

    assert driver.title != ""   '''

# tests/test_course_buy_catalog.py
import time, random
from src import config
from Pages.registration_page import RegistrationPage
from Pages.dashboard_page import DashboardPage
# If you already have a generator util, prefer:
# from src.generators import unique_email

def unique_email(domain: str = "cpraedcourse.com", prefix: str = "buycat_"):
    return f"{prefix}{int(time.time())}{random.randint(1000,9999)}@{domain}"

def test_course_buy_from_catalog(driver):
    email = unique_email()
    password = "Test1@1234"

    # 1) Register a brand-new corporate account
    reg = RegistrationPage(driver)
    (reg.start_from_home(config.BASE_URL)
       .go_to_group_discount()
       .start_registration(company="AHCA", email=email)
       .fill_basic_info_and_continue(
            first="Manish", last="Yadav",
            mobile="9876543210", password=password
        )
       # keep the order that worked for you:
       .pick_category_and_save(category_value="523", subcategory_value="1850")
       .accept_terms_and_submit())

    # 2) Ensure we’re on the v2 dashboard before using catalog/cart
    dash = DashboardPage(driver).go_to_v2_from_current()

    # 3) Buy from catalog (same as your existing flow)
    checkout = (dash.open_course_catalog()
                    .search_course("Suicide Prevention and Screening")
                    .add_first_result_to_cart()
                    .proceed_to_checkout())

    (checkout.fill_cardholder("Manish Yadav")
            .fill_card_number("4242424242424242")
            .fill_expiry("12/32")
            .fill_cvc("895")
            .choose_country("United States")
            .fill_postal("11230")
            .apply_promo("seg10")          # keep if valid for new orgs;
            .place_order())

    assert driver.title != ""
