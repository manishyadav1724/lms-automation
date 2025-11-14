import os
import time
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_verify_download_certificate(driver):
    wait = WebDriverWait(driver, 15)

    # Step 1: Open login page
    driver.get("https://staging-lms.gitview.net/login")

    # Step 2: Enter email
    wait.until(EC.presence_of_element_located(
        (By.NAME, "email"))
    ).send_keys("new_cerftication@cpraedcourse.com")

    # Step 3: Click "Continue"
    wait.until(EC.element_to_be_clickable(
        (By.ID, "btn-continue"))
    ).click()

    # Step 4: Enter password
    wait.until(EC.presence_of_element_located(
        (By.ID, "password"))
    ).send_keys("123456789")

    # Step 5: Click "Login"
    wait.until(EC.element_to_be_clickable(
        (By.ID, "btn-login"))
    ).click()

    # Step 6: Click on "Reporting"
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Reporting']"))
    ).click()
    driver.quit()


