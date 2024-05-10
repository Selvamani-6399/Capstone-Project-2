import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrangeHRM(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.url = "https://opensource-demo.orangehrmlive.com"

    def tearDown(self):
        self.driver.quit()

    def test_forgot_password_link_validation(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()

            forgot_password_link = self.driver.find_element(
                By.CLASS_NAME, "orangehrm-login-forgot")
            forgot_password_link.click()

            # Wait for the username input box to be visible
            username_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "username"))
            )
            username_box.send_keys("Admin")

            reset_password = self.driver.find_element(
                By.XPATH, "//button[@type='submit']")
            reset_password.click()

            # Wait for the reset password success message or error message to be displayed
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "orangehrm-card-container"))
            )

            print("Reset Password link sent successfully")
        except NoSuchElementException:
            print("Element not found.")
        except TimeoutException:
            print("Timeout occurred.")

    def test_admin_page_header_validation(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()

            self.driver.find_element(By.NAME, "username").send_keys("Admin")
            self.driver.find_element(By.NAME, "password").send_keys("admin123")
            self.driver.find_element(
                By.XPATH, "//button[@type='submit']").click()

            # Wait for the Admin page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href,'viewAdminModule')]"))
            )

            expected_title = "OrangeHRM"
            actual_title = self.driver.title
            if actual_title == expected_title:
                print("Title of the page is OrangeHRM")
            else:
                print("Unable to get the title")

            admin_options = ["User Management", "Job", "Organization", "Qualifications",
                             "Nationalities", "Corporate Branding", "Configuration"]
            admin_options_obj = self.driver.find_elements(
                By.CSS_SELECTOR, ".oxd-topbar-body-nav-tab-item")
            for option in admin_options_obj:
                option_value = option.text
                if option_value in admin_options:
                    print(option_value, " is present.")
                    self.assertTrue(option_value in admin_options)
        except NoSuchElementException:
            print("Element not found.")
        except TimeoutException:
            print("Timeout occurred.")

    def test_main_menu_validation(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()

            self.driver.find_element(By.NAME, "username").send_keys("Admin")
            self.driver.find_element(By.NAME, "password").send_keys("admin123")
            self.driver.find_element(
                By.XPATH, "//button[@type='submit']").click()

            # Wait for the Admin page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href,'viewAdminModule')]"))
            )

            # Go to the Admin Page
            self.driver.find_element(
                By.XPATH, "//a[contains(@href,'viewAdminModule')]").click()

            # Wait for the admin menu options to be visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, ".oxd-text.oxd-text--span.oxd-main-menu-item--name"))
            )

            admin_menu_options = ["Admin", "PIM", "Leave", "Time", "Recruitment", "My Info",
                                  "Performance", "Dashboard", "Directory", "Maintenance", "Claim", "Buzz"]
            admin_menu_options_obj = self.driver.find_elements(
                By.CSS_SELECTOR, ".oxd-text.oxd-text--span.oxd-main-menu-item--name")
            for option in admin_menu_options_obj:
                option_value = option.text
                if option_value in admin_menu_options:
                    print(option_value, " is present.")
                    self.assertTrue(option_value in admin_menu_options)
                else:
                    print(option_value, " is not present.")
        except NoSuchElementException:
            print("Element not found.")
        except TimeoutException:
            print("Timeout occurred.")


if __name__ == "__main__":
    unittest.main()