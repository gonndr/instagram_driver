from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os


class InstagramBot:
    def __init__(self):
        chromedriver_path = "/Users/goncalogomes/Code/Tools/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.follower_list = None

    def login(self):

        self.driver.get("https://www.instagram.com/accounts/login/")
        self.attempt(lambda: self.driver.find_element_by_xpath("/html/body/div[4]/div/div/button[2]").click()) #click permitions
        self.attempt(lambda: self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(os.environ["USERNAME"]))
        self.attempt(lambda: self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(os.environ["PASSWORD"]))
        self.attempt(lambda: self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(Keys.ENTER))
        self.attempt(lambda: self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()) # dont save info
        self.attempt(lambda: self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()) # turn off notifications
        return self.attempt(lambda: self.driver.find_element_by_xpath('/html/body/div[1]/section/main/section/div[3]/div[1]/div/div/div[2]/div[1]/div/div/a').text)


    def find_followers(self, page):
        self.attempt(lambda: self.driver.get(f"https://www.instagram.com/{page}"))
        self.attempt(lambda: self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span').click())
        popup = self.attempt(lambda: self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]'))
        # element_in_popup = self.attempt(lambda: popup.find_element_by_css_selector('div li div div div div div span a'))

        followers = self.scroll_till_end(popup)
        followers_names = []
        for person in followers:
            person_name = person.find_element_by_css_selector(" div div  div div span a span").text
            followers_names.append(person_name)

        return followers_names

    def find_following(self, page):
        self.attempt(lambda: self.driver.get(f"https://www.instagram.com/{page}"))
        self.attempt(lambda: self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div/span').click())
        popup = self.attempt(lambda: self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]'))
        # element_in_popup = self.attempt(
        #     lambda: popup.find_element_by_css_selector('div li div div div div div span a'))

        following = self.scroll_till_end(popup)
        following_names = []
        for person in following:
            person_name = person.find_element_by_css_selector(" div div  div div span a span").text
            following_names.append(person_name)

        return following_names

    def attempt(self, attempt_function):
        success = False
        while not success:
            try:
                time.sleep(1)
                element = attempt_function()
            except NoSuchElementException:
                print("not yet")
            else:
                success = True
                return element

    def scroll_till_end(self, element):
        success = False
        attempts = 0
        followers = []
        no_followers = 0
        while not success:
            time.sleep(1)
            # try:
            #     self.attempt(
            #         lambda: followers[-1].find_element_by_css_selector('div div div div div span a').send_keys(
            #             Keys.END))
            # except IndexError:
            #     self.attempt(lambda: element.find_element_by_css_selector('div li div div div div div span a').send_keys(Keys.END))
            self.driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);', element)
            time.sleep(1)
            followers = self.driver.find_elements_by_css_selector("div ul div li")
            no_followers_new = len(followers)
            print("Followers: ", no_followers_new)

            if no_followers_new == no_followers:
                attempts += 1
                print("Attempts: ", attempts)

                if attempts == 4: #change to 4
                    success = True
            else:
                attempts = 0
            no_followers = no_followers_new
        return followers
