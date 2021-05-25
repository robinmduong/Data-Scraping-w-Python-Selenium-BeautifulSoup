from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib
import urllib.request
import xlrd

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
baseurl = "https://www.cgwheels.com"

driver = webdriver.Chrome(PATH)

# CHANGE THIS LINE:
image_download_path = 'C:/Users/robin/48WS-Work/48ws-github/Manufacturer-Prod-images/cgw'

driver.get(baseurl)

def use_driver_current_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup

# CHANGE THIS LINE:
# file = open('optifuse_skus.txt') # Use this if you want to pull data from a text file
original_xlsx = 'CGW-new-manufacturer-to-upload-05.14.2021-all-products.xlsx' # Use this if you want to pull data from a .xlsx file
df = pd.DataFrame(pd.read_excel(original_xlsx))
# print(df.head())

for i, row in df.iterrows():
    # Search for Product
    sku = row['SKU #']
    # sku = row[1]['SKU #']
    search_bar = driver.find_element_by_id('searchbox')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)

    # Get All Details for 1 SKU
    image_file_name = str(sku) + ".jpg"
    try:
        image_src = WebDriverWait(driver, 1). until(EC.presence_of_element_located((By.XPATH, "//div//div//div//div//a//div//img"))).get_attribute("src")
        full_path = '../../../Manufacturer-Prod-Imgs/cgw/' + image_file_name
        urllib.request.urlretrieve(image_src, full_path)
        print('Image found: ', image_src)

    except Exception as e:
        print(e)
        print(str(sku) + ' - SKU not found. Image not added.')
        pass

    # print(df.head())