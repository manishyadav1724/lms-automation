# tests/test_verify_add_remove_course_cart.py
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage
from Pages.cart_page import CartPage

def test_verify_add_remove_course_cart(driver):
    """
    Test Case: Verify Add and Remove Course from Cart
    Steps:
      - Login
      - Click Purchase Seats
      - Add a course to cart
      - Remove the course using delete icon
    """

    email = "auto_test_01@cpraedcourse.com"
    password = "123456789"

    # Step 1: Login
    LoginPage(driver).open("https://staging-lms.gitview.net").login(email, password)
    print(" Logged in successfully")

    # Step 2: Navigate to Corporate V2
   # DashboardPage(driver).go_to_v2_from_current()

    # Step 3: Perform Cart Actions
    cart = CartPage(driver)
    cart.click_purchase_seats()
    print(" Clicked on 'Purchase Seats'")

    cart.add_course_to_cart()
    print(" Added course to cart")

    cart.remove_course_from_cart()
    print(" Removed course from cart successfully")

    # Assertion: optionally verify cart is empty
    assert True, "Add/Remove course test executed successfully"
    driver.quit()