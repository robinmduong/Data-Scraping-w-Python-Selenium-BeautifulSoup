import requests
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

import os
import re
import urllib.request

from selenium import webdriver # links with browser and carries out action
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = 'C:\Program Files (x86)\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)

baseurl = 'http://gemtexabrasives.com'
driver.get(baseurl)

# 'The HTTP headers User-Agent is a request header that allows a characteristic string that allows network protocol peers to identify the Operating System and Browser of the web-server. Your browser sends the user agent to every website you connect to' (geeksforgeeks.com)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

skus_to_find_list = ['20950300', '22045200', '71420', '25120853', '25120903', '25130853', '21530205', '25120923', '22045500', '25130903', '21530405', '21530605', '21830305', '50145600', '22050300', '70020003', '50145200', '50145300', '50145500', '50150200', '50150300', '20445200', '20445300', '20445500', '20450200', '20450300', '20450500', '22045300', '51120205', '51120305', '51130205', '51130305', '30220200', '30220300', '30520200', '30520300', '30530200', '22745300P', '70030001', '812745060H', '30230200', '44145500', '70045000', '70050000', '90000037', '44145300', '50145800', '51130505', '51130605', '51130805', '22745200', '22745302P', '812745080H', '812745120H', '64000', '50170200', '50170300', '70070000', '90000037', '22750600P', '22760600P', '25130923', '23812', '22745200P', '785901', '20645800', '812745036H', '712770080H', '812745060', '812745080', '8127450120', '9000037']

productlist = []
img_urls = []

def use_soup_current_url():
    r = requests.get(driver.current_url, headers = headers)
    print('Current URL:', driver.current_url)
    soup = BeautifulSoup(r.content, 'lxml')

for sku in skus_to_find_list:
    search_bar = driver.find_element_by_name('s')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)

    use_soup_current_url()

    try:
        read_more_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Read more'))
        )
        read_more_btn.click()
        use_soup_current_url()
        quick_overview = soup.find('div', itemprop='description').get_text()
        print(quick_overview)
    except:
        print('Product not found.')

''' DELETED CODE

product_pg_url = soup.find('a', string='Read more').get('href')

'''