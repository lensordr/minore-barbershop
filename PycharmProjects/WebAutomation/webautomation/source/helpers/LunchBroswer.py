import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CreateNewUser:
    def __init__(self):
        self.url = 'https://www.automationexercise.com/'
        self.driver = None

    def launch_browser(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        accept_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]/p')
        accept_button.click()

    def verify_homepage(self):
        home_page_text = self.driver.find_element(By.XPATH,"/html/body/section[2]/div[1]/div/div[1]/div/h2/text()")
        home_page_text = home_page_text.text
        if home_page_text == "CATEGORY":
            print("Home page is visible")

        else:
            print("Home page is not visible")


    def click_singUp(self):
        singUp_button = self.driver.find_element(By.XPATH,"/html/body/header/div/div/div/div[2]/div/ul/li[4]/a")
        singUp_button.click()




    def close_browser(self):
        # Close the browser
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    automation = CreateNewUser()
    try:
        automation.launch_browser()
        time.sleep(5)
        automation.verify_homepage()
        automation.click_singUp()
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        automation.close_browser()

