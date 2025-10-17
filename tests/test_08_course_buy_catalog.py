from src import config
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

    assert driver.title != ""
