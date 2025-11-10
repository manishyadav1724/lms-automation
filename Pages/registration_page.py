'''from selenium.webdriver.common.by import By
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
        return self '''

# Pages/registration_page.py
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

from base.base_page import BasePage


class RegistrationPage(BasePage):
    # ---------------- Locators ----------------
    GROUP_DISCOUNT_LINK   = (By.LINK_TEXT, "Group Discount")

    COMPANY_INPUT         = (By.NAME, "company_name")
    EMAIL_INPUT           = (By.NAME, "email")
    GET_STARTED_BTN_1     = (By.XPATH, "//button[normalize-space()='Get Started']")

    FIRST_NAME_INPUT      = (By.ID, "first_name")
    LAST_NAME_INPUT       = (By.NAME, "last_name")
    MOBILE_INPUT          = (By.NAME, "mobile")
    PASSWORD_INPUT        = (By.NAME, "password")
    GET_STARTED_BTN_2     = (By.CSS_SELECTOR, ".next-step.btn.btn-primary.next-grp.get-started")

    # Terms checkbox (multiple locators)
    TERMS_CHECKBOX_ID     = (By.ID, "term")
    TERMS_CHECKBOX_CLASS  = (By.CLASS_NAME, "custom-control-input")
    FINAL_SUBMIT_BTN      = (By.CSS_SELECTOR, ".btn.btn-submit-corporate.btn-primary.get-started")

    MODAL_BACKDROP_SHOW   = (By.CSS_SELECTOR, "div.modal-backdrop.fade.show")
    MODAL_BACKDROP_ANY    = "div.modal-backdrop"

    # Category page (as per your HTML snippet)
    CATEGORY_SELECT       = (By.ID, "category-select")
    SUBCATEGORY_SELECT    = (By.ID, "subcategory-select")

    # Save / Next / Continue (we’ll try multiple)
    SAVE_BUTTON           = (By.XPATH, "//button[normalize-space()='Save']")
    SAVE_FALLBACKS        = [
        (By.XPATH, "//button[normalize-space()='Save & Continue']"),
        (By.XPATH, "//button[normalize-space()='Next']"),
        (By.XPATH, "//button[contains(., 'Continue')]"),
        (By.CSS_SELECTOR, "button.btn.btn-primary"),
    ]

    # ---------------- Small helpers ----------------
    def _wait_clickable_any(self, locators, timeout=10):
        """Return the first WebElement that becomes clickable among given locators."""
        last_err = None
        for loc in locators:
            try:
                return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))
            except TimeoutException as e:
                last_err = e
        raise last_err or TimeoutException(f"None clickable: {locators}")

    # ---------------- Chainable public API ----------------
    def start_from_home(self, base_url: str):
        return self.visit(base_url)

    def go_to_group_discount(self):
        return self.click(self.GROUP_DISCOUNT_LINK)

    def start_registration(self, company: str, email: str):
        (
            self.type(self.COMPANY_INPUT, company)
                .type(self.EMAIL_INPUT, email)
                .click(self.GET_STARTED_BTN_1)
        )
        return self

    def fill_basic_info_and_continue(self, first: str, last: str, mobile: str, password: str):
        (
            self.type(self.FIRST_NAME_INPUT, first)
                .type(self.LAST_NAME_INPUT, last)
                .type(self.MOBILE_INPUT, mobile)
                .type(self.PASSWORD_INPUT, password)
                .click(self.GET_STARTED_BTN_2)
        )
        return self

    def pick_category_and_save(self, category_value: str, subcategory_value: str):
        # 1) Category
        cat = self.wait_clickable(self.CATEGORY_SELECT)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cat)
        Select(cat).select_by_value(category_value)

        # 2) Subcategory (wait until desired option appears)
        sub = self.wait_clickable(self.SUBCATEGORY_SELECT)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sub)

        def _option_loaded(_):
            try:
                return any(o.get_attribute("value") == subcategory_value for o in Select(sub).options)
            except Exception:
                return False

        WebDriverWait(self.driver, 10).until(_option_loaded)
        Select(sub).select_by_value(subcategory_value)

        # 3) Try to click Save/Next/Continue if available; else proceed silently
        candidate_locators = [
            (By.XPATH, "//button[normalize-space()='Save']"),
            (By.XPATH, "//button[normalize-space()='Save & Continue']"),
            (By.XPATH, "//button[normalize-space()='Next']"),
            (By.XPATH, "//button[contains(., 'Continue')]"),
            (By.CSS_SELECTOR, "button.btn.btn-primary"),
            (By.CSS_SELECTOR, "button[type='submit']"),
        ]

        save_btn = None
        for loc in candidate_locators:
            try:
                save_btn = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(loc))
                break
            except TimeoutException:
                continue

        if save_btn:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
            try:
                save_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", save_btn)
        # If no save-like button is present, we just continue; final submit will handle persistence.

        return self

    def accept_terms_and_submit(self):
        """Click the terms checkbox (via JS) using ID or class, then submit."""
        wait = WebDriverWait(self.driver, 20)

        # 1) checkbox: try id then class
        try:
            checkbox = wait.until(EC.presence_of_element_located((By.ID, "term")))
        except Exception:
            checkbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-control-input")))

        # JS click (stable)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", checkbox)

        # optional: verify and fallback to label
        try:
            if not self.driver.execute_script("return arguments[0].checked;", checkbox):
                try:
                    label = self.driver.find_element(By.CSS_SELECTOR, "label[for='term']")
                    self.driver.execute_script("arguments[0].click();", label)
                except Exception:
                    pass
        except Exception:
            pass

        # 2) submit button via JS
        submit = wait.until(EC.presence_of_element_located(self.FINAL_SUBMIT_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", submit)

        time.sleep(5)
        return self
