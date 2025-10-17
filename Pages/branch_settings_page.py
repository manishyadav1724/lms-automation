from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from base.base_page import BasePage

class BranchSettingsPage(BasePage):
    ADD_BRANCH_BTN = (By.XPATH, "//button[normalize-space()='Add Branch']")
    MODAL = (By.CSS_SELECTOR, "div.modal-content")

    FIRST_NAME = (By.XPATH, '//input[@placeholder="Admin First Name"]')
    LAST_NAME  = (By.XPATH, '//input[@placeholder="Admin Last Name"]')
    BRANCH_NAME = (By.NAME, "branch_name")
    EMAIL = (By.NAME, "email")
    LOCATION = (By.NAME, "branch_location")
    COUNTRY = (By.ID, "branch_country_id")
    STATE = (By.ID, "branch_province_id")
    CITY = (By.NAME, "city")
    ZIP = (By.NAME, "zipcode")
    SAVE = (By.XPATH, "//button[normalize-space()='Save Changes']")

    def add_branch(self, first, last, name, email, location, country_text, state_value, city, zip_code):
        self.click(self.ADD_BRANCH_BTN)
        self.wait_visible(self.MODAL)
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.BRANCH_NAME, name)
        self.type(self.EMAIL, email)
        self.type(self.LOCATION, location)

        from selenium.webdriver.support.select import Select
        Select(self.wait_visible(self.COUNTRY)).select_by_visible_text(country_text)
        Select(self.wait_visible(self.STATE)).select_by_value(state_value)

        self.type(self.CITY, city)
        self.type(self.ZIP, zip_code)
        self.js_click(self.SAVE)
        return self
