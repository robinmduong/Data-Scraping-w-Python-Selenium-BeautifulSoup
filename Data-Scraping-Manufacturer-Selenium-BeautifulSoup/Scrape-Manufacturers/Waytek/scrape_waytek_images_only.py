# Just to Scrape for Images on Manufacturer Site
# Searches each product by SKU in Search Bar to Create a Browser History of Each Page
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver # links w/ browser and carries out actions
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
baseurl = "http://www.waytekwire.com"

driver = webdriver.Chrome(PATH)
driver.get(baseurl)

def use_driver_current_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup

file = open('waytek_skus.txt')

skus_to_find = []
product_list = []

for line in file:
    line = line.replace('\n', '')
    skus_to_find.append(line)

# Go Into Each Individual SKU page and find image

for sku in skus_to_find :
    
    search_bar = driver.find_element_by_id('themeSearchText')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)   

    try:
        
        product_url = driver.find_elements_by_xpath("//div[contains(@class, 'itemDescription')]//h3//a[contains(text(), sku)]")[0]
        product_url.click()
        # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, '/images/items')]")))
    
    except:
        print('Product Not Found: ', sku)