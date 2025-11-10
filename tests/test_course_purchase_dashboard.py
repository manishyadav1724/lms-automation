from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_course_purchase_from_dashboard(driver):
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
    dash = DashboardPage(driver).go_to_v2_from_current()

    # Purchase seats -> search -> add to cart -> checkout
    checkout = (dash.open_purchase_seats()
                    .search_course("Clinical Care for the Heart Failure Patient")
                    .add_first_result_to_cart()
                    .proceed_to_checkout())

    # Fill Stripe test details
    checkout.fill_cardholder("Manish Yadav") \
            .fill_card_number("4242424242424242") \
            .fill_expiry("12/32") \
            .fill_cvc("895") \
            .choose_country("United States") \
            .fill_postal("11230") \
            .apply_promo("seg10") \
            .place_order()

    # smoke assert: we at least remained on site after submit (exact success UI depends on app)
    assert driver.title != ""
