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
baseurl = "http://www.optifuse.com"
# baseurl = "http://www.digikey.com"

driver = webdriver.Chrome(PATH)

# CHANGE THIS LINE:
image_download_path = 'C:/Users/robin/48WS-Work/48ws-github/Manufacturer-Prod-images/optifuse'

# Set the download directory for images
# options = webdriver.ChromeOptions()
# prefs = {'download.default_directory' : 'C:/Users/robin/48WS-Work/48ws-github/Manufacturer-Prod-images/optifuse'}
# options.add_experimental_option('prefs', prefs)
# driver = webdriver.Chrome(PATH, options=options)

driver.get(baseurl)

def use_driver_current_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup

# CHANGE THIS LINE:
# file = open('optifuse_skus.txt') # Use this if you want to pull data from a text file
original_xlsx = 'optifuse-original.xlsx' # Use this if you want to pull data from a .xlsx file
df = pd.DataFrame(pd.read_excel(original_xlsx))
print(df.head())

product_list = []

for i, row in df.iterrows():
    # Search for Product
    sku = row['SKU #']
    # sku = row[1]['SKU #']
    search_bar = driver.find_element_by_id('psearch')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)

    # Get All Details for 1 SKU
    try:
        product_url = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//td//div//a[contains(text(), sku)]")))
        product_url.click()
        
        # Get Product Quick Overview
        try:
            quick_overview = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//table//table//table//tr//td//font[contains(@size, '3')]"))).text
            print('Quick Overview: ', quick_overview)
        except:
            print('Quick overview not found.')
            quick_overview = ''

        # Get Product Details    
        try:
            details = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//table//table//td//p//font[contains(@size, '3')]"))).get_attribute('innerHTML')
            # details = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//table//table//td//p//font[contains(@size, '3')]"))).text-
            print('Details: ', details)
        except:
            print('Details not found.')
            details =''

        # Get Image Details
        image_file_name = sku + '.jpg'
        try:
            image_src = WebDriverWait(driver, 5). until(EC.presence_of_element_located((By.XPATH, "//table//table//table//a//img"))).get_attribute("src")
            full_path = '../../../Manufacturer-Prod-Imgs/optifuse/' + image_file_name
            urllib.request.urlretrieve(image_src, full_path)
            print('Image found: ', image_src)
        except Exception as e:
            print('Image not found. ', e)

        
        # Create 'product' object to represent SKU
        product = {
            'sku': sku,
            'image': image_file_name,
            'quick_overview': quick_overview,
            'details': details
        }

        print(product)
        product_list.append(product)

    except Exception as e:
        print(e)
        print('SKU not found.')
        pass

    # Update Pandas dataframe
    df.loc[i, 'Image'] = image_file_name
    df.loc[i, 'Quick Overview'] = quick_overview
    df.loc[i, 'Details'] = details

    print(df.head())

# Clean up extraneous characters
bad_characters = ['Â', '\\n', '\\r', '&nbsp', u00a0] #u00a0 is "&nbsp;"
df = df.replace(bad_characters, '')
print(df.head())

#CHANGE THIS LINE:
# Convert Pandas dataframe to Excel file
df.to_excel('scrape-optifuse-complete.xlsx')