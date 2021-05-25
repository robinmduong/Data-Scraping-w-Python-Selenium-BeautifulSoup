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
baseurl = "http://www.orangevise.com"

driver = webdriver.Chrome(PATH)

# CHANGE THIS LINE:
image_download_path = 'C:/Users/robin/48WS-Work/48ws-github/Manufacturer-Prod-images/orange-vise-imgs'

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
# original_xlsx = 'optifuse-original.xlsx' # Use this if you want to pull data from a .xlsx file
# df = pd.DataFrame(pd.read_excel(original_xlsx))
# print(df.head())


product_list = []

menu_items = ["bench-vises", "vises", "4-5-axis-vises", "jaws", "pallet-systems", "fixturing", "tombstones"]
nav_urls = []
for item in menu_items:
    full_url = baseurl + "/" + item
    nav_urls.append(full_url)

df = pd.DataFrame(columns = ['48WS.com', 'Category', 'SKU #', 'Product Name', 'Image', 'Manufacturer URL', 'Weight', 'Manufacturer', 'Description', 'Quick Overview', 'Group Name', 'Info/Size/Color', 'UPC'])

# Go into each category's page
for nav_url in nav_urls:
    # Search for Product
    driver.get(nav_url)

    # driver.find_elements_by_class_name("product-grid-container-wrapper")

    # Get individual product URLs
    product_urls = []
    product_url_container = driver.find_elements_by_class_name("product-item-link-overlay")
    for url in product_url_container:
        product_urls.append(url.get_attribute('href'))
    print("Product URLS: ", product_urls)

    # Go to each individual product page
    for product_url in product_urls:
        driver.get(product_url)
        print("Now scraping item: ", product_url)

        # Grab Product Details and Images

        # Get Product Name
        product_name = str(driver.find_element_by_class_name("product-title").text)

        # Set Image File Name
        formatted_product_name = product_name.replace(" ", "-")
        image_file_name = formatted_product_name + '.jpg'
        # print(image_file_name)
        
        # Download Image
        # try:
        #     image_src = WebDriverWait(driver, 3). until(EC.presence_of_element_located((By.XPATH, "//div//figure//a//img"))).get_attribute("src")
        #     full_path = '../../../Manufacturer-Prod-Imgs/orange-vise-imgs/' + image_file_name
        #     urllib.request.urlretrieve(image_src, full_path)
        #     print('Image found: ', image_src)
        # except Exception as e:
        #     print('Image not found. ', e)
            
        # Get Product Quick Overview
        try:
            quick_overview = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-description-container')]"))).get_attribute('innerHTML')
            print('Quick Overview: ', quick_overview)
        except:
            print('Quick overview not found.')
            quick_overview = ''

        # Get SKU
        try:
            sku = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//dd[contains(@itemprop, 'sku')]"))).text
            print('SKU: ', sku)
        except:
            print('SKU not found.')
            sku = ''


        # Get Weight
        # try:
        #     weight = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//dd[contains(@class, 'product-details-weight')]]"))).text
        # except:
        #     print('No Weight Found.')
        #     weight = ''
       
        # Create 'product' object to represent SKU
        product = {
            'sku': sku,
            'product_name': product_name,
            'image': image_file_name,
            'quick_overview': quick_overview,
            # 'details': details
        }

        print(product)
        product_list.append(product)

#     except Exception as e:
#         print(e)
#         print('SKU not found.')
#         pass


# Update Pandas dataframe
for i in range(len(product_list) - 1):
    df.loc[i, 'SKU #'] = product_list[i].get('sku')
    df.loc[i, 'Product Name'] = product_list[i].get('product_name')
    df.loc[i, 'Image'] = product_list[i].get('image')
    df.loc[i, 'Quick Overview'] = product_list[i].get('quick_overview')
print(df.head())

# # Clean up extraneous characters
# bad_characters = ['Â', '\\n', '\\r', '&nbsp', u00a0] #u00a0 is "&nbsp;"
# df = df.replace(bad_characters, '')
# print(df.head())

# #CHANGE THIS LINE:
# # Convert Pandas dataframe to Excel file
df.to_excel('scrape-orange-vise-complete-v1.xlsx')