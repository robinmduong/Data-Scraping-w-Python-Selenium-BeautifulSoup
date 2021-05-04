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

skus_to_find = []
product_list = []

for line in file:
    line = line.replace('\n', '')
    skus_to_find.append(line)