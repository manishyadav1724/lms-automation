from selenium.webdriver.common.by import By
from base.base_page import BasePage

class LearnersPage(BasePage):
    def summary_tile(self, label_text: str):
        return (By.XPATH, f'//div[@class="summary-label underline" and normalize-space()="{label_text}"]')

    def click_summary(self, label_text: str):
        self.js_click(self.summary_tile(label_text))
        return self
