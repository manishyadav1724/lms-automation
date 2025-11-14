'''from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- helpers ---
    def _scroll_into_view(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", el)
        except Exception:
            pass
        try:
            ActionChains(self.driver).move_to_element(el).perform()
        except Exception:
            pass

    def _set_value_js(self, el, text: str):
        # clear value and set via JS + fire input/change events
        self.driver.execute_script(
            "arguments[0].value=''; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));", el
        )
        self.driver.execute_script(
            "arguments[0].value=arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            el, text
        )

    # --- core actions ---
    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self._scroll_into_view(el)
        el.click()
        return el

    def type(self, locator, text: str):
        # Wait for visibility (not just presence)
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self._scroll_into_view(el)

        # Try native clear/send_keys first
        try:
            el.clear()
        except WebDriverException:
            # Some inputs don’t support clear(); ignore
            pass

        try:
            el.send_keys(text)
            return el
        except (ElementNotInteractableException, WebDriverException):
            # Fallback to JS set if still not interactable
            self._set_value_js(el, text)
            return el

    def wait_visible(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self._scroll_into_view(el)
        return el

    def wait_gone(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def js_click(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self._scroll_into_view(el)
        self.driver.execute_script("arguments[0].click();", el)
        return el'''


# base/base_page.py
'''from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # basic helpers
    def visit(self, url: str):
        self.driver.get(url)
        self.driver.maximize_window()
        return self

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        el = self.wait_clickable(locator)
        el.click()
        return self

    def js_click(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        return self

    def type(self, locator, text: str, clear=True):
        el = self.wait_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)
        return self

    def select_by_value(self, locator, value: str):
        el = self.wait_clickable(locator)
        Select(el).select_by_value(value)
        return self

    def select_by_visible_text(self, locator, text: str):
        el = self.wait_clickable(locator)
        Select(el).select_by_visible_text(text)
        return self

    def wait_invisible(self, locator, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        return self

    def remove_if_present(self, css_selector: str):
        # removes element via JS if present; safe no-op if absent
        try:
            el = self.driver.find_element("css selector", css_selector)
            self.driver.execute_script("arguments[0].remove();", el)
        except Exception:
            pass
        return self


#new code add
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def wait_clickable_any(self, locators, timeout=10):
    """Return the first locator that becomes clickable, else raise."""
    last_err = None
    for loc in locators:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))
        except TimeoutException as e:
            last_err = e
    raise last_err or TimeoutException(f"None clickable: {locators}") '''

# base/base_page.py
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, os


class BasePage:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.default_timeout = timeout          # <-- add this line
        self.wait = WebDriverWait(driver, timeout)

    # basic helpers
    def visit(self, url: str):
        self.driver.get(url)
        self.driver.maximize_window()
        return self

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        el = self.wait_clickable(locator)
        el.click()
        return self

    def js_click(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        return self

    def type(self, locator, text: str, clear=True):
        el = self.wait_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)
        return self

    def select_by_value(self, locator, value: str):
        el = self.wait_clickable(locator)
        Select(el).select_by_value(value)
        return self

    def select_by_visible_text(self, locator, text: str):
        el = self.wait_clickable(locator)
        Select(el).select_by_visible_text(text)
        return self

    def wait_invisible(self, locator, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        return self

    def remove_if_present(self, css_selector: str):
        try:
            el = self.driver.find_element("css selector", css_selector)
            self.driver.execute_script("arguments[0].remove();", el)
        except Exception:
            pass
        return self

    # --- optional helper for screenshot-on-timeout diagnostics ---
    def _save_screenshot(self, name_suffix: str):
        ts = time.strftime("%Y%m%d_%H%M%S")
        dirname = "screenshots"
        os.makedirs(dirname, exist_ok=True)
        fname = os.path.join(dirname, f"{name_suffix}_{ts}.png")
        try:
            self.driver.save_screenshot(fname)
        except Exception:
            pass
        return fname


# Additional utility
def wait_clickable_any(self, locators, timeout=10):
    """Return the first locator that becomes clickable, else raise."""
    last_err = None
    for loc in locators:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))
        except TimeoutException as e:
            last_err = e
    raise last_err or TimeoutException(f"None clickable: {locators}")


