from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from base.base_page import BasePage

class RegistrationPage(BasePage):
    # Step 1 (Group Discount page)
    COMPANY = (By.NAME, "company_name")
    EMAIL = (By.NAME, "email")
    GET_STARTED = (By.XPATH, "//button[normalize-space()='Get Started']")

    # Step 2 (Basic form)
    FIRST = (By.ID, "first_name")
    LAST = (By.NAME, "last_name")
    MOBILE = (By.NAME, "mobile")
    PASSWORD = (By.NAME, "password")
    NEXT_GET_STARTED = (By.CSS_SELECTOR, ".next-step.btn.btn-primary.next-grp.get-started")

    # Terms + final submit
    TERMS_CHECKBOX = (By.CLASS_NAME, "custom-control-input")
    FINAL_SUBMIT = (By.CSS_SELECTOR, ".btn.btn-submit-corporate.btn-primary.get-started")

    # Overlays
    MODAL_BACKDROP_VISIBLE = (By.CSS_SELECTOR, "div.modal-backdrop.fade.show")
    MODAL_BACKDROP = (By.CSS_SELECTOR, "div.modal-backdrop")

    # Category screen
    CATEGORY_SELECT = (By.ID, "categorySelect")
    SUBCATEGORY_SELECT = (By.ID, "subCategorySelect")
    SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save']")

    # Language + logout
    LANG_DROPDOWN = (By.CLASS_NAME, "gt_selector")
    LANG_SPANISH = (By.XPATH, "//option[text()='Spanish'] | //div[text()='Spanish']")
    EDIT_PROFILE_BTN = (By.CLASS_NAME, "name_btn")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")

    def start_from_home(self, base_url: str):
        self.driver.get(base_url)
        return self

    def go_to_group_discount(self):
        from selenium.webdriver.common.by import By
        self.click((By.LINK_TEXT, "Group Discount"))
        return self

    def start_registration(self, company: str, email: str):
        self.type(self.COMPANY, company)
        self.type(self.EMAIL, email)
        self.click(self.GET_STARTED)
        return self

    def fill_basic_info_and_continue(self, first: str, last: str, mobile: str, password: str):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.MOBILE, mobile)
        self.type(self.PASSWORD, password)
        self.click(self.NEXT_GET_STARTED)
        return self

    def accept_terms_and_submit(self):
        el = self.wait_visible(self.TERMS_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", el)
        self.click(self.FINAL_SUBMIT)
        self.wait_gone(self.MODAL_BACKDROP_VISIBLE)
        try:
            modal = self.driver.find_element(*self.MODAL_BACKDROP)
            self.driver.execute_script("arguments[0].remove();", modal)
        except Exception:
            pass
        return self

    def pick_category_and_save(self, category_value: str, subcategory_value: str):
        cat = self.wait_visible(self.CATEGORY_SELECT)
        Select(cat).select_by_value(category_value)
        sub = self.wait_visible(self.SUBCATEGORY_SELECT)
        Select(sub).select_by_value(subcategory_value)
        self.click(self.SAVE_BTN)
        return self

    def switch_language_to_spanish(self):
        self.js_click(self.LANG_DROPDOWN)
        self.click(self.LANG_SPANISH)
        return self

    def logout_via_profile(self):
        self.click(self.EDIT_PROFILE_BTN)
        self.click(self.LOGOUT_LINK)
        return self
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from base.base_page import BasePage

class RegistrationPage(BasePage):
    # Step 1 (Group Discount page)
    COMPANY = (By.NAME, "company_name")
    EMAIL = (By.NAME, "email")
    GET_STARTED = (By.XPATH, "//button[normalize-space()='Get Started']")

    # Step 2 (Basic form)
    FIRST = (By.ID, "first_name")
    LAST = (By.NAME, "last_name")
    MOBILE = (By.NAME, "mobile")
    PASSWORD = (By.NAME, "password")
    NEXT_GET_STARTED = (By.CSS_SELECTOR, ".next-step.btn.btn-primary.next-grp.get-started")

    # Terms + final submit
    TERMS_CHECKBOX = (By.CLASS_NAME, "custom-control-input")
    FINAL_SUBMIT = (By.CSS_SELECTOR, ".btn.btn-submit-corporate.btn-primary.get-started")

    # Overlays
    MODAL_BACKDROP_VISIBLE = (By.CSS_SELECTOR, "div.modal-backdrop.fade.show")
    MODAL_BACKDROP = (By.CSS_SELECTOR, "div.modal-backdrop")

    # Category screen
    CATEGORY_SELECT = (By.ID, "categorySelect")
    SUBCATEGORY_SELECT = (By.ID, "subCategorySelect")
    SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save']")

    # Language + logout
    LANG_DROPDOWN = (By.CLASS_NAME, "gt_selector")
    LANG_SPANISH = (By.XPATH, "//option[text()='Spanish'] | //div[text()='Spanish']")
    EDIT_PROFILE_BTN = (By.CLASS_NAME, "name_btn")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")

    def start_from_home(self, base_url: str):
        self.driver.get(base_url)
        return self

    def go_to_group_discount(self):
        from selenium.webdriver.common.by import By
        self.click((By.LINK_TEXT, "Group Discount"))
        return self

    def start_registration(self, company: str, email: str):
        self.type(self.COMPANY, company)
        self.type(self.EMAIL, email)
        self.click(self.GET_STARTED)
        return self

    def fill_basic_info_and_continue(self, first: str, last: str, mobile: str, password: str):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.MOBILE, mobile)
        self.type(self.PASSWORD, password)
        self.click(self.NEXT_GET_STARTED)
        return self

    def accept_terms_and_submit(self):
        el = self.wait_visible(self.TERMS_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", el)
        self.click(self.FINAL_SUBMIT)
        self.wait_gone(self.MODAL_BACKDROP_VISIBLE)
        try:
            modal = self.driver.find_element(*self.MODAL_BACKDROP)
            self.driver.execute_script("arguments[0].remove();", modal)
        except Exception:
            pass
        return self

    def pick_category_and_save(self, category_value: str, subcategory_value: str):
        cat = self.wait_visible(self.CATEGORY_SELECT)
        Select(cat).select_by_value(category_value)
        sub = self.wait_visible(self.SUBCATEGORY_SELECT)
        Select(sub).select_by_value(subcategory_value)
        self.click(self.SAVE_BTN)
        return self

    def switch_language_to_spanish(self):
        self.js_click(self.LANG_DROPDOWN)
        self.click(self.LANG_SPANISH)
        return self

    def logout_via_profile(self):
        self.click(self.EDIT_PROFILE_BTN)
        self.click(self.LOGOUT_LINK)
        return self
