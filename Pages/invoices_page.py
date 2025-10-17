from selenium.webdriver.common.by import By
from base.base_page import BasePage

class InvoicesPage(BasePage):
    DROPDOWN_BTN = (By.CSS_SELECTOR, ".btn-group .dropdown-toggle")
    DOWNLOAD_LINK = (By.XPATH, '//a[contains(@href, "/download")]')

    def download_first_invoice(self):
        self.click(self.DROPDOWN_BTN)
        self.click(self.DOWNLOAD_LINK)
        return self
