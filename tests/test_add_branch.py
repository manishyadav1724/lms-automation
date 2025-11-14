from src import config
from Pages.login_page import LoginPage
from Pages.dashboard_page import DashboardPage

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_add_branch(driver):
    from src import config
    from Pages.login_page import LoginPage
    from Pages.dashboard_page import DashboardPage

    # Login
    LoginPage(driver).open(config.BASE_URL).login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)

    # Navigate to Branch Settings (stay in V1)
    page = DashboardPage(driver).open_branch_settings()
    time.sleep(3)
    # Wait for Add Branch button
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Add Branch"]'))
    )

    #  Generate a unique branch email using timestamp
    timestamp = int(time.time())
    unique_email = f"branch_{timestamp}@example.com"

    # (Optional) Or use random number if you prefer:
    # unique_email = f"branch_{random.randint(1000,9999)}@example.com"

    # Add branch
    page.add_branch(
        first="John",
        last="Doe",
        name=f"Main Training Branch {timestamp}",
        email=unique_email,  #  unique email each run
        location="Texas HQ, US",
        country_text="United States",
        state_value="32",
        city="Shaktinagar",
        zip_code="23434",
    )

    assert True
    driver.quit()
