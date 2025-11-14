# Pages/cart_page.py
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from base.base_page import BasePage

class CartPage(BasePage):
    """
    CartPage: robust operations to Purchase Seats, Add to Cart, and Remove from Cart.
    """

    # Locators
    PURCHASE_SEATS_BTN = (By.XPATH, "//button[normalize-space()='Purchase Seats']")
    ADD_TO_CART_BTN = (By.XPATH, "//div[contains(@class,'course-card')]//button[@type='button' and normalize-space()='Add To Cart']")
    # Prefer the button element that contains a trash icon; adjust if your markup differs
    DELETE_BUTTONS = (By.XPATH, "//button[contains(@class,'js-remove-cart') or contains(@class,'remove-cart') or .//i[contains(@class,'fa-trash') or contains(@class,'trash')]]")
    CART_PANEL = (By.XPATH, "//div[contains(@class,'cart-panel') or contains(@class,'cart-modal') or contains(@id,'cart')]")
    CART_ITEM_ROWS = (By.XPATH, "//div[contains(@class,'cart-item') or contains(@class,'cart-row') or contains(@class,'cart-items')]")

    def _save_screenshot_and_raise(self, name_suffix: str):
        ts = time.strftime("%Y%m%d_%H%M%S")
        dirname = "screenshots"
        os.makedirs(dirname, exist_ok=True)
        fname = os.path.join(dirname, f"{name_suffix}_{ts}.png")
        try:
            self.driver.save_screenshot(fname)
        except Exception:
            pass
        raise TimeoutException(f"Timed out waiting for element ({name_suffix}). Screenshot saved to: {fname}")

    def click_purchase_seats(self, timeout: int = None):
        t = timeout if timeout is not None else getattr(self, "default_timeout", 15)
        try:
            el = WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(self.PURCHASE_SEATS_BTN))
            el.click()
            return self
        except TimeoutException:
            self._save_screenshot_and_raise("purchase_seats_btn")

    def add_course_to_cart(self, timeout: int = None):
        """
        Click 'Add To Cart' for the first available course card, then wait for cart panel or update.
        """
        t = timeout if timeout is not None else getattr(self, "default_timeout", 15)
        try:
            el = WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))
            try:
                el.click()
            except Exception:
                # fallback: scroll and JS click
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                self.driver.execute_script("arguments[0].click();", el)

            # Wait a short while for cart UI to update (mini-cart, panel, badge, etc.)
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.CART_PANEL))
            except Exception:
                # fallback: small sleep if no explicit panel is present
                time.sleep(1)
            return self
        except TimeoutException:
            self._save_screenshot_and_raise("add_to_cart_btn")

    def remove_course_from_cart(self, timeout: int = None):
        """
        Find a delete button in the cart and click it robustly. If no button is found or click fails,
        save a screenshot and raise for diagnostics.
        """
        t = timeout if timeout is not None else getattr(self, "default_timeout", 15)
        try:
            # Ensure cart UI is visible if it exists
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.CART_PANEL))
            except Exception:
                # It's fine if there's no dedicated cart panel; continue searching
                pass

            # Collect candidate delete buttons
            candidates = self.driver.find_elements(*self.DELETE_BUTTONS)
            if not candidates:
                # try alternate path inside cart rows
                candidates = self.driver.find_elements(By.XPATH,
                    "//div[contains(@class,'cart-item') or contains(@class,'cart-row')]//button[.//i[contains(@class,'fa-trash') or contains(@class,'trash')]]"
                )

            if not candidates:
                # nothing found — save screenshot and raise
                self._save_screenshot_and_raise("delete_icon_not_found")

            # choose the first visible & enabled candidate
            btn = None
            for c in candidates:
                try:
                    if c.is_displayed() and c.is_enabled():
                        btn = c
                        break
                except Exception:
                    continue
            if btn is None:
                # no visible/enabled button found; pick the first candidate and try anyway
                btn = candidates[0]

            # scroll and attempt to click
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            except Exception:
                pass
            time.sleep(0.5)

            try:
                # prefer standard click
                btn.click()
            except StaleElementReferenceException:
                # element replaced in DOM — re-find and click
                time.sleep(0.5)
                new_candidates = self.driver.find_elements(*self.DELETE_BUTTONS)
                if not new_candidates:
                    self._save_screenshot_and_raise("delete_icon_stale_and_not_found")
                btn = new_candidates[0]
                try:
                    btn.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", btn)
            except Exception:
                # fallback to JS click for stubborn overlays
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    self._save_screenshot_and_raise("delete_click_failed")

            # Optionally: wait for cart row to disappear (if your app removes row instantly)
            try:
                WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(self.CART_ITEM_ROWS))
            except Exception:
                # not fatal; continue
                pass

            return self

        except TimeoutException:
            self._save_screenshot_and_raise("delete_icon")


