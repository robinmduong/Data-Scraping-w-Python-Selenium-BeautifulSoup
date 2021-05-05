# This successfully visits each individual product page in the SKU list

from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
baseurl = "http://www.zoro.com"

driver = webdriver.Chrome(PATH)
driver.get(baseurl)

def use_driver_current_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup

file = open('zoro_skus.txt')

skus_to_find = []
product_list = []

for line in file:
    line = line.replace('\n', '')
    skus_to_find.append(line)

for sku in skus_to_find:
    
    search_bar = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@accesskey, 'S')]")))
    time.sleep(2)
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)

    try:
        cross_click=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class='svg-icon zcl-icon zcl-icon--small'])[2]")))
        cross_click.click()
    except Exception as e:
        print(e)
        pass