import requests
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

import os
import re
import urllib.request #Py3 doesn't have urllib

from selenium import webdriver # links w/ browser and carries out actions
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

baseurl = "http://www.waytekwire.com"
driver.get(baseurl)

#Populate the SKUs to be found

file = open('waytek_skus.txt')

skus_to_find = []
for line in file:
    line = line.replace('\n', '')
    skus_to_find.append(line)
  
#Sample List of SKUS:
skus_to_find_test = ['WL16-8', 'WG18-12']

headers = {
    # CHROME 80 on WINDOWS: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=breadcrumbs
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

def use_soup_current_url():
    r = requests.get(driver.current_url, headers = headers)
    print('Current URL:', driver.current_url)
    soup = BeautifulSoup(r.content, 'lxml')

for sku in skus_to_find:
    search_bar = driver.find_element_by_id('themeSearchText')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)   
    use_soup_current_url()
    try:
        product_url = driver.find_elements_by_xpath("//div[contains(@class, 'itemDescription')]//h3//a[contains(text(), sku)]")[0]
        product_url.click()
        use_soup_current_url()
        try:
            # overview_tab = driver.find_elements_by_xpath("//span[contains(text(), 'Overview')]")
            # print(overview_tab)
            # overview_tab.click()
            # quick_overview = WebDriverWait(driver, 5).until(
            #     EC.presence_of_element_located(By.TAG_NAME,'description')
            # )
            # quick_overview = soup.find_element_by_xpath("//span[@itemprop='description']")
            # quick_overview = soup.find_element_by_xpath("//span[contains(@itemprop, 'description')]")
            quick_overview = soup.find('div', itemprop='description').get_text()
            # quick_overview = soup.find_element_by_xpath("//span")
            # print(quick_overview)
        except:
            print('No Quick Overview Found.')
        try:
            # regex = '^[A-Z][0-9]+-'
            # img_file = re.match(regex, sku).group() + '.jpg'
            img_file = sku + '.jpg'
            print(img_file)
        except:
            print('No Image Found')
        product = {
            'image': image,
            'product_name': product_name or '',
            'quick_overview': quick_overview or '',
            'details': details,    
        }
    except:
        print('Product not found.')