from selenium.webdriver.support.ui import WebDriverWait
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
        return el
