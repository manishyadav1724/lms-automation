# Pages/common_widgets.py
from selenium.webdriver.common.by import By
from base.base_page import BasePage

class LanguageSwitcher(BasePage):
    LANG_DROPDOWN = (By.CLASS_NAME, "gt_selector")
    # Supports either <option> or <div> renderings
    def language_option(self, text: str):
        return (By.XPATH, f"//option[normalize-space()='{text}'] | //div[normalize-space()='{text}']")

    def switch_to(self, language_text: str):
        # sometimes needs scroll + JS click on busy UIs
        self.js_click(self.LANG_DROPDOWN)
        self.click(self.language_option(language_text))
        return self
