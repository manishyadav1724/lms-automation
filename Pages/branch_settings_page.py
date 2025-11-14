'''from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from base.base_page import BasePage
#checking new push
class BranchSettingsPage(BasePage):
    ADD_BRANCH_BTN = (By.XPATH, '//button[normalize-space()="Add Branch"]')
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
        return self '''

# Pages/branch_settings_page.py
import os
import time
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from base.base_page import BasePage


import os
import time
import uuid
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, StaleElementReferenceException
)

class BranchSettingsPage(BasePage):
    """
    BranchSettingsPage - uses modal-scoped exact locators (including OR-style XPaths)
    and provides robust filling (with JS fallback). Generates unique email if needed.
    """

    # Primary (simple) locators derived from your original script
    ADD_BRANCH_BTN = (By.XPATH, "//button[normalize-space()='Add Branch']")
    MODAL_CONTAINER = (By.CSS_SELECTOR, "div.modal-content")

    # Simple field locators (use name / placeholder / id where available)
    FIRST_NAME = (By.XPATH, '//input[@placeholder="Admin First Name"]')
    LAST_NAME = (By.XPATH, '//input[@placeholder="Admin Last Name"]')
    BRANCH_NAME = (By.NAME, "branch_name")
    BRANCH_EMAIL = (By.NAME, "email")
    BRANCH_LOCATION = (By.NAME, "branch_location")
    COUNTRY_SELECT = (By.ID, "branch_country_id")
    STATE_SELECT = (By.ID, "branch_province_id")
    CITY = (By.NAME, "city")
    ZIP = (By.NAME, "zipcode")
    SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save Changes' or normalize-space()='Save']")

    # Robust modal-scoped OR-style XPaths (fallbacks)
    FIRST_NAME_XPATH = ".//input[@placeholder='Admin First Name' or @name='first_name' or contains(@placeholder,'First') or contains(@aria-label,'First')]"
    LAST_NAME_XPATH = ".//input[@placeholder='Admin Last Name' or @name='last_name' or contains(@placeholder,'Last') or contains(@aria-label,'Last')]"
    BRANCH_NAME_XPATH = ".//input[@name='branch_name' or contains(@placeholder,'Branch Name') or contains(@aria-label,'Branch')]"
    BRANCH_EMAIL_XPATH = ".//input[@placeholder='Eg branch@xyz.com' or @name='email' or contains(@aria-label,'Email')]"
    BRANCH_LOCATION_XPATH = ".//input[@placeholder='NewYork' or @name='location' or contains(@aria-label,'Location')]"
    COUNTRY_SELECT_XPATH = ".//select[@id='branch_country_id' or @name='country_id' or @name='country']"
    STATE_SELECT_XPATH = ".//select[@id='branch_province_id' or @name='state' or @name='province']"
    CITY_XPATH = ".//input[@name='city' or contains(@placeholder,'City') or contains(@aria-label,'City')]"
    ZIP_XPATH = ".//input[@name='zip' or @name='zipcode' or @name='postal' or contains(@placeholder,'Zip') or contains(@aria-label,'Zip')]"
    SAVE_BTN_XPATH = ".//button[normalize-space()='Save' or normalize-space()='Add' or contains(@class,'save-branch') or contains(@class,'btn-primary')]"

    # Global fallback selectors (if modal-scoped fails)
    COUNTRY_SELECT_GLOBAL = (By.XPATH, "//select[@id='branch_country_id' or @name='country_id' or @name='country']")
    STATE_SELECT_GLOBAL = (By.XPATH, "//select[@id='branch_province_id' or @name='state' or @name='province']")

    def _save_screenshot_and_raise(self, name_suffix):
        ts = time.strftime("%Y%m%d_%H%M%S")
        dirname = "screenshots"
        os.makedirs(dirname, exist_ok=True)
        png = os.path.join(dirname, f"{name_suffix}_{ts}.png")
        html = os.path.join(dirname, f"{name_suffix}_{ts}.html")
        try:
            self.driver.save_screenshot(png)
            with open(html, "w", encoding="utf-8") as fh:
                fh.write(self.driver.page_source)
        except Exception:
            pass
        raise TimeoutException(f"Timed out/failure in '{name_suffix}'. Saved: {png}, {html}")

    def _js_set_value(self, el, value):
        try:
            self.driver.execute_script("""
                var el = arguments[0];
                var val = arguments[1];
                if (typeof el.focus === 'function') { el.focus(); }
                el.value = val;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            """, el, value)
            return True
        except Exception:
            return False

    def _find_in_modal(self, modal_root, relative_xpath, timeout=5):
        """Find element by relative XPath inside modal_root (returns element or raises)."""
        end = time.time() + timeout
        last_exc = None
        while time.time() < end:
            try:
                el = modal_root.find_element(By.XPATH, relative_xpath)
                if el and el.is_displayed():
                    return el
            except Exception as e:
                last_exc = e
            time.sleep(0.25)
        raise NoSuchElementException(f"Element not found in modal: {relative_xpath}. Last exc: {last_exc}")

    def open_add_branch_modal(self, timeout=12):
        """Click Add Branch and return modal root element."""
        try:
            el = WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable(self.ADD_BRANCH_BTN))
            try:
                el.click()
            except Exception:
                # JS fallback click & scroll into view
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    self.driver.execute_script("arguments[0].click();", el)
                except Exception:
                    pass
        except Exception:
            # fallback: try any button text variant (lowercase match) via alternative XPath
            try:
                alt = WebDriverWait(self.driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'add branch')]"))
                )
                try:
                    alt.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", alt)
            except Exception:
                self._save_screenshot_and_raise("add_branch_button_not_found")

        # Wait for modal container or modal-content to appear
        try:
            modal_el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.MODAL_CONTAINER))
            # choose modal root: prefer the modal-content element itself
            modal_root = modal_el
        except Exception:
            # fallback: try to find a header text 'Add Branch' inside DOM and choose its ancestor container
            try:
                header = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(text()), 'Add Branch')]"))
                )
                try:
                    modal_root = header.find_element(By.XPATH, "ancestor::div[.//input or .//select or .//textarea][1]")
                except Exception:
                    modal_root = header.find_element(By.XPATH, "ancestor::div[1]")
            except Exception:
                self._save_screenshot_and_raise("add_branch_modal_not_visible")

        return modal_root

    def _fill_input(self, modal_root, xpath, value, field_name):
        """Generic fill helper: try send_keys, else JS set."""
        try:
            # When xpath begins with '.' treat as relative; else treat as tuple locator
            if isinstance(xpath, str) and xpath.startswith(".//"):
                el = self._find_in_modal(modal_root, xpath, timeout=6)
            else:
                # expect a tuple locator like (By.NAME, 'email')
                if isinstance(xpath, tuple):
                    el = WebDriverWait(modal_root, 6).until(EC.visibility_of_element_located(xpath))
                else:
                    raise ValueError("xpath must be relative xpath string or locator tuple")
        except NoSuchElementException:
            raise
        except Exception as e:
            print(f"[warn] locating {field_name} raised: {e}")
            raise

        try:
            # click/focus
            try:
                el.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                except Exception:
                    pass

            # attempt clear if supported
            try:
                el.clear()
            except Exception:
                pass

            # try send_keys
            try:
                el.send_keys(value)
                return True
            except Exception:
                # js fallback
                if self._js_set_value(el, value):
                    return True
                else:
                    raise
        except StaleElementReferenceException:
            # try once more
            time.sleep(0.25)
            return self._fill_input(modal_root, xpath, value, field_name)
        except Exception as e:
            print(f"[warn] failed to set field {field_name}: {e}")
            raise

    def add_branch(self,
                   first="John",
                   last="Doe",
                   name=None,
                   email=None,
                   location="Texas HQ, US",
                   country_text="United States",
                   state_value=None,
                   city="Shaktinagar",
                   zip_code="23434",
                   timeout=18):
        """
        Open modal, fill fields using modal-scoped exact locators,
        and save. Auto-generates branch name/email if not provided.
        """
        # generate unique values if not provided
        unique_id = uuid.uuid4().hex[:6]
        if not email:
            email = f"branch_{unique_id}@example.com"
        if not name:
            name = f"QA_AutoBranch_{unique_id}"
        if state_value is None:
            state_value = random.randint(1, 50)

        modal_root = self.open_add_branch_modal(timeout=12)

        # small wait for animations / inputs to be interactable
        time.sleep(0.6)

        try:
            # Try primary (simple) locators first, fall back to modal-scoped XPaths if necessary
            try:
                self._fill_input(modal_root, self.FIRST_NAME, first, "first_name")
            except Exception:
                self._fill_input(modal_root, self.FIRST_NAME_XPATH, first, "first_name")

            try:
                self._fill_input(modal_root, self.LAST_NAME, last, "last_name")
            except Exception:
                self._fill_input(modal_root, self.LAST_NAME_XPATH, last, "last_name")

            try:
                # branch name by NAME
                self._fill_input(modal_root, self.BRANCH_NAME, name, "branch_name")
            except Exception:
                self._fill_input(modal_root, self.BRANCH_NAME_XPATH, name, "branch_name")

            try:
                self._fill_input(modal_root, self.BRANCH_EMAIL, email, "branch_email")
            except Exception:
                self._fill_input(modal_root, self.BRANCH_EMAIL_XPATH, email, "branch_email")

            try:
                self._fill_input(modal_root, self.BRANCH_LOCATION, location, "branch_location")
            except Exception:
                self._fill_input(modal_root, self.BRANCH_LOCATION_XPATH, location, "branch_location")

            # country select - prefer modal-scoped select under modal_root
            country_selected = False
            try:
                # try modal-scoped select via relative XPath
                country_el = modal_root.find_element(By.XPATH, self.COUNTRY_SELECT_XPATH)
                Select(country_el).select_by_visible_text(country_text)
                country_selected = True
            except Exception:
                try:
                    # try primary simple locator (global)
                    sel = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(self.COUNTRY_SELECT))
                    Select(sel).select_by_visible_text(country_text)
                    country_selected = True
                except Exception:
                    try:
                        # final fallback global XPath
                        sel = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(self.COUNTRY_SELECT_GLOBAL))
                        Select(sel).select_by_visible_text(country_text)
                        country_selected = True
                    except Exception:
                        print("[warn] country select not found/failed")

            # state select - same multi-fallback approach
            try:
                state_el = modal_root.find_element(By.XPATH, self.STATE_SELECT_XPATH)
                Select(state_el).select_by_value(str(state_value))
            except Exception:
                try:
                    sel = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(self.STATE_SELECT))
                    Select(sel).select_by_value(str(state_value))
                except Exception:
                    try:
                        sel = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(self.STATE_SELECT_GLOBAL))
                        Select(sel).select_by_value(str(state_value))
                    except Exception:
                        print("[warn] state select not found/failed")

            # city & zip
            try:
                self._fill_input(modal_root, self.CITY, city, "city")
            except Exception:
                self._fill_input(modal_root, self.CITY_XPATH, city, "city")

            try:
                self._fill_input(modal_root, self.ZIP, zip_code, "zip")
            except Exception:
                self._fill_input(modal_root, self.ZIP_XPATH, zip_code, "zip")

            # click Save inside modal if present
            save_clicked = False
            try:
                # prefer the modal-scoped save button
                save_btn = modal_root.find_element(By.XPATH, self.SAVE_BTN_XPATH)
                try:
                    save_btn.click()
                    save_clicked = True
                except Exception:
                    try:
                        self.driver.execute_script("arguments[0].click();", save_btn)
                        save_clicked = True
                    except Exception:
                        pass
            except Exception:
                # try global save button
                try:
                    save_btn_global = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(self.SAVE_BTN))
                    try:
                        save_btn_global.click()
                        save_clicked = True
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", save_btn_global)
                        save_clicked = True
                except Exception:
                    pass

            if not save_clicked:
                # last resort: click by XPath anywhere (global)
                try:
                    self.click((By.XPATH, "//button[normalize-space()='Save Changes' or normalize-space()='Save']"))
                    save_clicked = True
                except Exception:
                    self._save_screenshot_and_raise("save_button_not_found_or_click_failed")

            # wait for modal to disappear - check modal container invisibility
            try:
                WebDriverWait(self.driver, timeout).until_not(EC.visibility_of_element_located(self.MODAL_CONTAINER))
            except Exception:
                # if modal container wasn't used, wait for any "Add Branch" header to vanish
                try:
                    WebDriverWait(self.driver, 6).until_not(
                        EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(text()), 'Add Branch')]"))
                    )
                except Exception:
                    # allow test to continue but log and screenshot
                    self._save_screenshot_and_raise("modal_did_not_close")

            return {"branch_name": name, "email": email}

        except NoSuchElementException as e:
            print("[error] element not found during add_branch:", e)
            self._save_screenshot_and_raise("element_missing_in_modal")
        except Exception as e:
            print("[error] unexpected error in add_branch:", e)
            self._save_screenshot_and_raise("add_branch_failed")
