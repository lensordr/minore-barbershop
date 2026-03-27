import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.automationexercise.com/'
driver = webdriver.Firefox()
driver.get(url)
accept_button = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]/p')
accept_button.click()



