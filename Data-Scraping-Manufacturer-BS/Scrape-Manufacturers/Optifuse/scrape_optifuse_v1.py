from bs4 import BeautifulSoup
import pandas as pd
import re
import xlrd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
baseurl = "http://www.optifuse.com"
# baseurl = "http://www.digikey.com"

driver = webdriver.Chrome(PATH)
driver.get(baseurl)

def use_driver_current_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup

# file = open('optifuse_skus.txt')

original_xlsx = 'optifuse-original.xlsx'
df_updated = pd.DataFrame(pd.read_excel(original_xlsx))
print(df_updated.head())
# sku_column - df_updated[usecols=""]

product_list = []


for row in df_updated.iterrows():
    # Search for Product
    sku = row[1]['SKU #']
    print(sku)
    search_bar = driver.find_element_by_id('psearch')
    # search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, 'psearch')])")))
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)

    try:
        cross_click = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "(//*[@class, 'MuiSvgIcon-root'])[2]")))
        cross_click.click()
    except Exception as e:
        print(e)
        print('No Product Found.')
        pass

    #Get Product Details
    try:
        product_details = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table[contains(@id, 'product-attributes')]")))
    except Exception as e:
        print(e)
        print('No Product Details Found.')
        pass

    image = sku + '.jpg'

    # Create product object to represent this SKU
    product = {
        'sku': sku,
        'image': image,
        'quick_overview': quick_overview,
        # 'details': details
    }

    print(product)

    #Add new product to product list
    product_list.append(product)

    # Clean up extraneous characters

    bad_characters = ['Â', '\\n', '\\r']

    for line in df_updated:
        line = line.replace('\n', '')
        skus_to_find.append(line)
