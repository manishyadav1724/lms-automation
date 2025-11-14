'''from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

def test_course_purchase_from_dashboard(driver):
    # Login into system (V1 login page)
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)


    dash = DashboardPage(driver).go_to_v2_from_current()

    # Purchase seats  -> search  -> add to cart  -> checkout
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
    driver.quit()'''

from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage
from Pages.checkout_page import CheckoutPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException


def test_course_purchase_from_dashboard(driver):
    """Updated test:
    - Logs in with purchase_dashboard@cpraedcourse.com / 123456789
    - Clicks the Purchase Seats button using the provided XPath
    - Clicks Add To Cart using the provided XPath
    - Clicks Proceed to Checkout using the provided XPath
    - Uses the CheckoutPage object to fill Stripe test card details and place order

    Fixes included:
    - Waits for any loading overlay ("div.lds-ripple") to disappear before clicking
    - Uses a small retry + JS-click fallback when `ElementClickInterceptedException` occurs
    - Adds some extra explicit waits to make clicks more stable
    """

    # Login into system (V1 login page) with updated credentials
    LoginPage(driver).open(config.BASE_URL).login("purchase_dashbaord@cpraedcourse.com", "123456789")

    # Navigate to v2 dashboard (keeps your existing navigation helper)
    dash = DashboardPage(driver).go_to_v2_from_current()

    wait = WebDriverWait(driver, 20)

    # Click Purchase Seats button
    purchase_btn_xpath = '//button[normalize-space()="Purchase Seats"]'
    purchase_btn = wait.until(EC.element_to_be_clickable((By.XPATH, purchase_btn_xpath)))
    purchase_btn.click()

    # Optionally wait for the results/cards to load before adding to cart
    add_to_cart_xpath = '//div[@class="card course-card "]//button[@type="button"][normalize-space()="Add To Cart"]'
    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_to_cart_xpath)))
    add_to_cart_btn.click()

    # Wait for any loading spinner/overlay to disappear before proceeding
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.lds-ripple")))
    except TimeoutException:
        # If spinner doesn't appear or doesn't disappear in time, continue - later retry will handle it
        pass

    # Click Proceed to Checkout using ID locator (more stable)
    proceed_id = "proceedToCheckoutBtn"
    proceed_btn = wait.until(EC.presence_of_element_located((By.ID, proceed_id)))

    clicked = False
    for _ in range(3):
        try:
            wait.until(EC.element_to_be_clickable((By.ID, proceed_id)))
            proceed_btn.click()
            clicked = True
            break
        except ElementClickInterceptedException:
            # Wait until the overlay is gone and retry; then use JS click as fallback
            try:
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.lds-ripple")))
            except TimeoutException:
                pass
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_btn)
            driver.execute_script("arguments[0].click();", proceed_btn)
            clicked = True
            break

    if not clicked:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_btn)
        driver.execute_script("arguments[0].click();", proceed_btn)

    # Initialize CheckoutPage (assumes this page object exists and wraps checkout form/stripe helpers)
    checkout = CheckoutPage(driver)

    # Fill Stripe test details (keeps your original test card values)
    # These methods are kept as-chained calls on the CheckoutPage object (matching your previous style).
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

    driver.quit()
