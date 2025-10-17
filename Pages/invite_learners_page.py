from selenium.webdriver.common.by import By
from base.base_page import BasePage

class InviteLearnersPage(BasePage):
    ADD_ROW_BTN = (By.CSS_SELECTOR, "button.plus_btn.js-add-row.mb-4[aria-label='Add row']")
    SEND_INVITE = (By.ID, "btnSendInvite")

    def _nth(self, locator, index: int):
        els = self.wait.until(lambda d: d.find_elements(*locator))
        return els[index]

    FNAME = (By.XPATH, '//div[@class="f-name"]//input[@placeholder="Eg John"]')
    LNAME = (By.XPATH, '//div[@class="l-name"]//input[@placeholder="Doe"]')
    EMAIL = (By.XPATH, '//div[@class="e-mail"]//input[@placeholder="johndoe@xyz.com"]')

    def add_rows_and_fill(self, count: int, email_factory):
        for i in range(count):
            if i > 0:
                self.click(self.ADD_ROW_BTN)
            self._nth(self.FNAME, i).send_keys(f"John{i+1}")
            self._nth(self.LNAME, i).send_keys(f"Doe{i+1}")
            self._nth(self.EMAIL, i).send_keys(email_factory())
        return self

    def send_invites(self):
        self.click(self.SEND_INVITE)
        return self
