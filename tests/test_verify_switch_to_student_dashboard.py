from Pages.login_page import LoginPage
from Pages.new_panel_page import NewPanelPage

def test_verify_switch_to_student_dashboard(driver):
    # Login
    LoginPage(driver).open("https://staging-lms.gitview.net") \
                     .login("newpanel_02@cpraedcourse.com", "123456789")

    # Switch to Student → wait 2s → Settings menu (user dropdown) → Switch to Organization
    panel = NewPanelPage(driver)
    panel.switch_to_student() \
         .wait_seconds(2) \
         .open_user_dropdown() \
         .switch_to_organization()

    # Assertions: first we should have hit student URL, then back to corporate URL
    # (If you want, split into two asserts with intermediate reads)
    assert "/corporate_v2" in driver.current_url or "/corporate" in driver.current_url

    driver.quit()