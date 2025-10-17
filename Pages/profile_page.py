from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from base.base_page import BasePage

class Header(BasePage):
    def avatar_by_alt(self, alt_text: str):
        return (By.XPATH, f"//div[@role='button']//img[@alt='{alt_text}']")

    EDIT_PROFILE_LINK = (By.XPATH, "//a[contains(normalize-space(.), 'Edit Profile')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(normalize-space(.), 'Logout')]")
    NOTIFICATIONS_BTN = (By.XPATH, "//a[@aria-label='Notifications']")

    def open_profile_menu(self, alt_text: str = "John Doe"):
        self.click(self.avatar_by_alt(alt_text))
        return self

    def go_to_edit_profile(self):
        self.click(self.EDIT_PROFILE_LINK)
        return EditProfilePage(self.driver)

    def logout(self):
        # assumes the profile menu is already open
        self.click(self.LOGOUT_LINK)
        return self

    def open_notifications(self):
        self.click(self.NOTIFICATIONS_BTN)
        return self


class EditProfilePage(BasePage):
    EDIT_PROFESSIONAL_INFO_ICON = (By.XPATH, "//span[@data-bs-target='#professionalinformation']//img")
    CATEGORY_SELECT = (By.ID, "selectCategory")
    SUBCATEGORY_SELECT = (By.ID, "selectSubCategory")
    SAVE_CHANGES_BTN = (By.CLASS_NAME, "purchase-btn")

    def open_professional_info(self):
        self.click(self.EDIT_PROFESSIONAL_INFO_ICON)
        return self

    def set_professional_category(self, category_text: str, subcategory_text: str):
        cat = self.wait_visible(self.CATEGORY_SELECT)
        Select(cat).select_by_visible_text(category_text)
        sub = self.wait_visible(self.SUBCATEGORY_SELECT)
        Select(sub).select_by_visible_text(subcategory_text)
        return self

    def save_changes(self):
        try:
            self.click(self.SAVE_CHANGES_BTN)
        except Exception:
            self.js_click(self.SAVE_CHANGES_BTN)
        return self
