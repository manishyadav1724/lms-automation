from selenium.webdriver.common.by import By
from base.base_page import BasePage
from Pages.checkout_page import CheckoutPage
from Pages.learners_page import LearnersPage
from Pages.invoices_page import InvoicesPage
from Pages.branch_settings_page import BranchSettingsPage
from Pages.invite_learners_page import InviteLearnersPage


class DashboardPage(BasePage):
    # sidebar / buttons
    PURCHASE_SEATS_BTN = (By.XPATH, '//button[contains(text(), "Purchase Seats")]')
    COURSE_CATALOG_LINK = (By.XPATH, "//nav[@id='sidebar']//a[contains(@class,'nav-link')][normalize-space()='Course Catalog']")
    LEARNERS_LINK = (By.XPATH, '//a[contains(@href, "/corporate_v2/learners")]')
    INVOICES_LINK = (By.XPATH, '//a[contains(., "Invoices")]')
    BRANCH_SETTINGS_LINK = (By.XPATH, "//a[normalize-space(text())='Branch Settings']")
    INVITE_LEARNERS_BTN = (By.XPATH, "//button[contains(text(),'Invite Learners')]")

    # catalog + common
    SEARCH_BOX = (By.XPATH, "//input[@id='searchInput']")
    ADD_TO_CART_BTN_VISIBLE = (By.XPATH, "//button[normalize-space()='Add To Cart']")
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(@class,'add-cart-btn') and contains(text(),'Add To Cart')]")
    PROCEED_CHECKOUT_BTN = (By.XPATH, "//a[@class='btn btn-primary w-100 order_btn']")

    def go_to_v2_from_current(self):
        current = self.driver.current_url
        v2 = current.replace("/corporate", "/corporate_v2")
        self.driver.get(v2)
        return self

    def open_purchase_seats(self):
        self.click(self.PURCHASE_SEATS_BTN)
        return self

    def open_course_catalog(self):
        self.click(self.COURSE_CATALOG_LINK)
        return self

    def search_course(self, name: str):
        sb = self.wait_visible(self.SEARCH_BOX)
        sb.clear()
        sb.send_keys(name)
        from selenium.webdriver.common.keys import Keys
        sb.send_keys(Keys.ENTER)
        return self

    def add_first_result_to_cart(self):
        self.wait_visible(self.ADD_TO_CART_BTN_VISIBLE)
        self.js_click(self.ADD_TO_CART_BTN)
        return self

    def proceed_to_checkout(self):
        self.click(self.PROCEED_CHECKOUT_BTN)
        #from Pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    def open_learners(self):
        self.js_click(self.LEARNERS_LINK)
        from .learners_page import LearnersPage
        return LearnersPage(self.driver)

    def open_invoices(self):
        self.js_click(self.INVOICES_LINK)
        from .invoices_page import InvoicesPage
        return InvoicesPage(self.driver)

    def open_branch_settings(self):
        self.js_click(self.BRANCH_SETTINGS_LINK)
        from .branch_settings_page import BranchSettingsPage
        return BranchSettingsPage(self.driver)

    def open_invite_learners(self):
        self.click(self.INVITE_LEARNERS_BTN)
        #from .invite_learners_page import InviteLearnersPage
        return InviteLearnersPage(self.driver)
