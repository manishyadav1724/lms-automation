from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from base.base_page import BasePage
import time

class NewPanelPage(BasePage):
    # Locators
    SWITCH_TO_STUDENT = (By.ID, "switchToStudentBtn")
    USER_DROPDOWN = (By.ID, "dropdownUserAction")
    SWITCH_TO_ORG = (By.XPATH, "//a[contains(@href, 'switch_to_organization')]")

    # Actions
    def switch_to_student(self):
        self.js_click(self.SWITCH_TO_STUDENT)
        # wait for student dashboard url
        self.wait.until(EC.url_contains("/panel/student"))
        return self

    def wait_seconds(self, seconds: float = 2.0):
        time.sleep(seconds)
        return self

    def open_user_dropdown(self):
        self.js_click(self.USER_DROPDOWN)
        return self

    def switch_to_organization(self):
        self.js_click(self.SWITCH_TO_ORG)
        # wait for corporate url (v2 or legacy)
        try:
            self.wait.until(EC.url_contains("/corporate_v2"))
        except Exception:
            self.wait.until(EC.url_contains("/corporate"))
        return self
