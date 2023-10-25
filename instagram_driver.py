from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time
import os

WAIT_TIMEOUT = 6
IG_BASE_URL = "https://www.instagram.com"
IG_LOGIN_URL = f"{IG_BASE_URL}/accounts/login"
IG_PROFILE_URL = f"{IG_BASE_URL}/{os.environ['USERNAME']}"
FOLLOWERS_MODAL_XPATH = '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]'
FOLLOWING_MODAL_XPATH = '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]'


def locate_by_xpath(xpath):
    return By.XPATH, xpath


def locate_by_name(name):
    return By.NAME, name


def expect_element_visible(xpath):
    return EC.visibility_of_element_located(locate_by_xpath(xpath))


def expect_element_invisible(xpath):
    return EC.invisibility_of_element(locate_by_xpath(xpath))


def expect_element_clickable(xpath=None, name=None):
    if name is None:
        return EC.element_to_be_clickable(locate_by_xpath(xpath))
    else:
        return EC.element_to_be_clickable((locate_by_name(name)))


def get_handles_list_from_dialog(dialog):
    return dialog.find_elements(*locate_by_xpath(".//a//div/div/span"))


class InstagramDriver:
    def __init__(self):
        chromedriver_path = os.environ["DRIVER_PATH"]
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=chrome-user-data")
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

    def wait_driver_until(self, condition):
        return WebDriverWait(self.driver, WAIT_TIMEOUT).until(condition)

    def wait_until_dialog_closed(self):
        return self.wait_driver_until(expect_element_invisible(xpath=f"//*[@role='dialog']"))

    def get_dialog_by_type(self, dialog_type):
        modal_xpath = FOLLOWERS_MODAL_XPATH if dialog_type == 'followers' else FOLLOWING_MODAL_XPATH
        return self.wait_driver_until(expect_element_visible(xpath=modal_xpath))

    def get_element_by_exact_text(self, name):
        return self.wait_driver_until(expect_element_clickable(xpath=f"//*[text()='{name}']"))

    def get_element_by_name(self, name):
        return self.wait_driver_until(expect_element_clickable(name=name))

    def get_dialog_height(self, dialog):
        return self.driver.execute_script('return arguments[0].scrollHeight;', dialog)

    def scroll_dialog_to_bottom(self, dialog):
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', dialog)

    def get_has_dialog_loaded_new_data(self, dialog, initial_height):
        return self.get_dialog_height(dialog) != initial_height

    def login(self):
        self.driver.get(IG_LOGIN_URL)
        self.get_element_by_exact_text('Allow all cookies').click()
        self.wait_until_dialog_closed()
        self.get_element_by_name('username').send_keys(os.environ["USERNAME"])
        self.get_element_by_name('password').send_keys(os.environ["PASSWORD"])
        self.get_element_by_exact_text('Log in').click()
        self.get_element_by_exact_text('Not now').click()
        self.get_element_by_exact_text('Not Now').click()

    def navigate_to_profile(self):
        self.driver.get(IG_PROFILE_URL)

    def get_list_of(self, list_type):
        self.driver.get(f"{IG_PROFILE_URL}/{list_type}")
        dialog = self.get_dialog_by_type(list_type)
        time.sleep(2)
        self.scroll_till_end_of_dialog(dialog)
        handles_list = get_handles_list_from_dialog(dialog)
        return [handle.text for handle in handles_list]

    def scroll_till_end_of_dialog(self, dialog):
        is_dialog_end = False
        while not is_dialog_end:
            initial_dialog_height = self.get_dialog_height(dialog)
            self.scroll_dialog_to_bottom(dialog)
            try:
                self.wait_driver_until(
                    lambda driver: self.get_has_dialog_loaded_new_data(dialog, initial_dialog_height))
            except TimeoutException:
                is_dialog_end = True
