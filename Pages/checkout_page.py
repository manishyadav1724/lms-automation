from selenium.webdriver.common.by import By
from base.base_page import BasePage

class CheckoutPage(BasePage):
    CARDHOLDER = (By.ID, "cardholder_name")
    CARD_NUMBER_IFRAME = (By.XPATH, "//div[@id='card-number']//iframe")
    EXP_IFRAME = (By.XPATH, "//div[@id='card-expiry']//iframe")
    CVC_IFRAME = (By.XPATH, "//div[@id='card-cvc']//iframe")

    COUNTRY_SELECT = (By.ID, "Field-countryInput")
    POSTAL = (By.ID, "postal_code")
    PROMO = (By.ID, "promocode")
    SUBMIT = (By.ID, "submit")

    def fill_cardholder(self, name: str):
        self.type(self.CARDHOLDER, name)
        return self

    def _type_in_iframe(self, iframe_locator, input_name, value):
        iframe = self.wait_visible(iframe_locator)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element(By.NAME, input_name).send_keys(value)
        self.driver.switch_to.default_content()

    def fill_card_number(self, number: str):
        self._type_in_iframe(self.CARD_NUMBER_IFRAME, "cardnumber", number)
        return self

    def fill_expiry(self, exp_mm_yy: str):
        self._type_in_iframe(self.EXP_IFRAME, "exp-date", exp_mm_yy)
        return self

    def fill_cvc(self, cvc: str):
        self._type_in_iframe(self.CVC_IFRAME, "cvc", cvc)
        return self

    def choose_country(self, visible_text: str):
        sel = self.wait_visible(self.COUNTRY_SELECT)
        for opt in sel.find_elements(By.TAG_NAME, "option"):
            if opt.text.strip() == visible_text:
                opt.click()
                break
        return self

    def fill_postal(self, code: str):
        self.type(self.POSTAL, code)
        return self

    def apply_promo(self, code: str):
        try:
            self.type(self.PROMO, code)
        except Exception:
            pass
        return self

    def place_order(self):
        self.click(self.SUBMIT)
        return self
