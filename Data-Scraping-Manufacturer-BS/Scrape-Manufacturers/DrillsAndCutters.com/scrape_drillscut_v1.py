import requests
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

import re
import urllib.request

from selenium import webdriver # links w/ browser and carries out actions
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

baseurl = "http://www.drillsandcutters.com"
driver.get(baseurl) #They don't have a designated products page

headers = {
    # CHROME 80 on WINDOWS: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=breadcrumbs
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

skus_to_find_list = ["CBDXXL20014B", "KDF17"]

# sku_list = ["CBDXXL20014B","KFD17","KFD18","KFD21","KFD24","KFD26","KFD39","DWDA/CX63/16","DWDA/CX61/8","KFD35","DAM4X5/16","DAM3X1/8"," DAM4X3/16"," DAM4X7/32","DAM4X1/4","DAM4X3/8","DAM4X3/8","DAM4X7/16","DAM4X1/2"," DWDA/CX611/64","MMO7/32-2FSE","DWDA/CX611/64","DWCT307","D/ADE1/4","KFDRSD3/8X5/8","KFDRSD3/8X3/4","DWDA/CX121/4","DWDCOZ","DWDCOU","DWDCOA","DWT57151","DWT54928","DWT54779","DWT54759","DWDCOR","DWDCO7","DWDCO28","DWDCO29","DWDCO30","DWDCO30","DWT64007","DWT60891","DWT60829","KFD29J-PC","DWC5-530-133","DWC5-530-905","DWT54329","DWT54356","DWT54393","DWTT3X.5","DWTT4X.7","DWTT5X.8","DWTT6X1","DWTT7X1","DWTT8X1","DWTT8X1.25","DWTT10X1.25","DWTT10X1.5","DWTT12X1.75","DWTT14X2","DWT60999","KFD25","DWDCOK","DWDCOH","DWDCOD","DWDCOB","DWDCOA","DWDCO2","DWDCO1","DWDCO19","DWDCO22","DWDCO24","DWT54584","DWT54739","DWTHX1224","DWTHX1032","DWTHX1024","DWTHX832","DWTHX632","DWDA/CX67/16","DWT57076","DWT57072","DWT57085","DWT57089","DWDCOY","DWDCOE","DWDCOF","DWDCO25","DWDCO18","DWDCO59","DWDRSD7/8","DWT54225","DWT60793","DWT60797","DWT60891","DWT60887","DWRR3/16","DWRR3/8","DWRR1/4","DWTHX71614","DWTHX114","DWDCO20","DWDCO23","DWDCO26","DWDCO27","DWDCO52","DWDCO5","DWDCOG","DWDCOP","DWRRCO5/16","DWTHSHEX51618","DWTHSHEX3824","DWTHSHEX91618","DWTHSHEX91612","DWTHSHEX5811","DWT54520","DWT54597","DWT54728","DWT54767","DWT54892","DWT54925","DWT54935","DWTST3/8-18B","DWTST3/4-14B","DWDCOS","DWDCO8","DWDCO35","DWDCO40","DWDCO3","T/A64007","DWRRCO3/16","DWTHX71620","DWDCOL","DWDCOT","DWDCO16","DWDCO12","DWDCO6","DWDCO21","DWDCO36","DWT54455","DWTB8X1.25","DWTB6X1","DWRRCO1/4","DWRRCO3/8","DWT54358","DWT54279","DWT54331","MMO1/4-4FSE","MMO1/2-4FSE","MMO3/4-4FSE","MMO1/4-4FSE-BN","MMO1/2-4FSE-BN","MMO3/4-4FSE-BN","DWDCO37","DWDCO45","DWDCO31","DWDCO17","GLBCOX121/4","DWT54471","DWTHXNPT34","DWTHXNPT1INCH","DWT54387","DWDCOX","DWDCOW","DWDCOC","DWDCON","DWTHX3816","DWT57129","DWDCOQ","DWT57097","DWT57104"]

productlinks = []
itemlist = []

for sku in skus_to_find_list:
    search_bar = driver.find_element_by_name('q')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)
    r = requests.get(driver.current_url, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    quick_overview = soup.find('div', class_='productView-description-tabContent')
    details = soup.find('div', class_='productView-addition-tabContent')
    image_file_name = re.findall(r"[\w]+", sku)[0] + '.jpg'
    print(image_file_name)