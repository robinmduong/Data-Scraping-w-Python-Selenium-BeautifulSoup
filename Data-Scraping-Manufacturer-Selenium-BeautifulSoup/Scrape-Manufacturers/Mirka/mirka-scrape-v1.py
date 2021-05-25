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
baseurl = "http://www.mirka-online.com"

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
original_xlsx = 'mirka-original.xlsx' # Use this if you want to pull data from a .xlsx file
df = pd.DataFrame(pd.read_excel(original_xlsx))
# print(df.head())

product_list = []

for i, row in df.iterrows():

    # Search for Product
    sku = row['SKU #']       # sku = row[1]['SKU #']
    
    search_bar = driver.find_element_by_name('q')
    search_bar.clear()
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)

    # Clear Out Search Bar
    # try:
    #     cross_click=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class=")))
    #     cross_click.click()
    # except Exception as e:
    #     print(e)
    #     pass

    # Get All Details for 1 SKU
    try:
        # Click Into Individual Product Page
        try:
            product_url = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//li//div//a[contains(text(), sku)]")))
            product_url.click()
        except:
            "No individual product URL found."
        # Get Product Quick Overview
        # try:
        #     quick_overview = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'product.info.description)]"))).text
        #     print('Quick Overview: ', quick_overview)
        # except:
        #     print('Quick overview not found.')
        #     quick_overview = ''

        # Get Product Details    
        try:
            details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[2]/div/div[4]/div[2]/div/div[2]"))).get_attribute('innerHTML')
            print('Details: ', details)
        except:
            print('Details not found.')
            details =''

        # # Get Image Details
        image_file_name = str(sku) + '.jpg'
        try:
            image_src = WebDriverWait(driver, 10). until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'fotorama__img')]"))).get_attribute("src")
            full_path = '../../../Manufacturer-Prod-Imgs/mirka/' + image_file_name
            urllib.request.urlretrieve(image_src, full_path)
            print('Image found: ', image_src)
        except Exception as e:
            print('Image not found. ', e)

        
        # Create 'product' object to represent SKU
        # product = {
        #     'sku': sku,
        #     'image': image_file_name,
        #     # 'quick_overview': quick_overview,
        #     'details': details
        # }

        # print(product)
        # product_list.append(product)

        try:
            # Update Pandas dataframe
            df.loc[i, 'Image'] = image_file_name
            # df.loc[i, 'Quick Overview'] = quick_overview
            df.loc[i, 'Details'] = details

            # print(df.head())

        except:
            print('Could not update data frame')

    except Exception as e:
        print(e)
        print('SKU not found.')
        pass


# Clean up extraneous characters
df = df.replace({'\\r\\n':' ', '\\r':' ', '\\n':' ', '&176;':'°', '&nbsp;':' ', 'nbsp;':' ',
                '&#176;':'°', '&#153;':'™', '&#174;':'®', '&trade;':'™', '<[^<]+?>' : '',
                '\(bul\)' : '', '&quot;' : '"', 'Â':'', '\\n':' ', '&nbsp;':' ', '&nbsp':' ', '                ':''}
                , regex=True)
print(df.head())

#CHANGE THIS LINE:
# Convert Pandas dataframe to Excel file
# df.to_excel('scrape-mirka-complete.xlsx')
df.to_excel('scrape-mirka-complete-2.xlsx')