from selenium.webdriver.common.by import By
from base.base_page import BasePage

class LoginPage(BasePage):
    EMAIL = (By.ID, "email")
    CONTINUE = (By.ID, "btn-continue")
    PASSWORD = (By.ID, "password")
    LOGIN = (By.ID, "btn-login")

    def open(self, base_url: str):
        self.driver.get(base_url.rstrip('/') + "/login")
        return self

    def login(self, email: str, password: str):
        self.type(self.EMAIL, email)
        self.click(self.CONTINUE)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN)
        return self
