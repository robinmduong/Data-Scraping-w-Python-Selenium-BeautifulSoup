import requests
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

import urllib.request

from selenium import webdriver # links up with browser and performs actions
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

baseurl = "http://www.allfuses.com"
driver.get("http://www.allfuses.com/all-products")

headers = {
    # CHROME 80 on WINDOWS: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=breadcrumbs
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

products_to_find_list = ["FRN-R-20", "FLNR-009", "ATQ20", "BAF-25","ATM5","ATM1/2","OTM6","GFN1-1/8","OTM5","BAF-1/2","SBS8/10","TRM5","ATQ1/4","GFN1/2","ATQ10","ATQR1/4","ATQR4","ATQR1-1/2","ATQR30","AGC-10","GMA-2.5-R", "GMA-1.5-R","ATMR1","GMA-500-R","ATQR12","GFN-3","GFN-1","ATDR15","GMA-1-R","A6D100R","TRS200R","TR400R","TRS100R","RFS60","TR90R","TRS90R","OT40","TRS7R","TR2R","TR3R","TRS3R","AJT7","AJT30","AJT25","TR40R","TRS50R","ATQR8","ATQR10","TR25R","KTK-R-12","KTK-R-15","KTK-R-20","KTK-R-25","FNM-10","FNM-15","ATQR20","ATQR15","LP-CC-20","A4BY1200","A4J100","A4J200","A50P40-4","A50Q540-4","A70QS63-22F","ABC-10","ABC-25","ABC-8","AGC-12","AGC-15","AGC-1-R","AGC-25","AGC-3","AGC-4","AGC-5","AGC-7-1/2","AGU-2","AGX-7","AJT10","AJT12","AJT15","AJT175","AJT20","AJT35","AJT40","AJT5","AJT50","AJT6","AJT60","ATDR30","ATM2","ATQ15","ATQ2","ATQ30","ATQ5","ATQR5","BAF-2","BAF-5","BBS-8/10","BLF1/2","FLM-002","FLM-005","FLNR-010","FLNR-100","FLNR-200","FLNR-025","FLNR-030","FLNR-090","FLQ-.250","FLQ-002","FLQ-003","FLSR-100","FLSR-005","FLSR-050","FNA-1/2","FNA-1","FNA-3","FNM-2","FNM-5","FNQ-1/4","FNQ-8/10","FNQ-10","FNQ-15","FNQ-2","FNQ-25","FNQ-3","FNQ-4","FNQ-5","FNQ-6","FNQ-R-1/4","FRN-R-100","FRN-R-10","FRN-R-125","FRN-R-15","FRN-R-2","FRN-R-200","FRN-R-3","FRN-R-3-1/2","FRN-R-30","FRN-R-40","FRN-R-5","FRN-R-50","FRN-R-6","FRN-R-60","FRN-R-8","FRS-R-10","FRS-R-100","FRS-R-125","FRS-R-150","FRS-R-2-1/2","FRS-R-20","FRS-R-30","FRS-R-35","FRS-R-40","FRS-R-5","FRS-R-50","FRS-R-60","FRS-R-80","FWP-125A","FWP-100","FWP-25A22F","GAB5","GFN12","GFN2","GGC1/2","GLR10","GLR-2","GMA-15-R","GMC-500MA","IDSR-7","JTD-015","JTD-030","JTD-080","JTD-090","KAC-60","KLDR-004","GGC2","KLDR-01.5","KTK-8","KTK-R-1","KTK-R-2","KTK-R-3","KTK-R-4","KTK-R-6","LP-CC-12","LP-CC-2","LP-CC-4","LP-CC-5","LPJ-150SP","LPJ-175SP","LPJ-20SP","LPJ-200SP","LPJ-30SP","LPJ-35SP","LPJ-40SP","LPJ-45SP","LPJ-50SP","LPJ-60SP","LPJ-80SP","LPS-RK-100SP","LPS-RK-200SP","MDA-4-R","MDA-25-R","MDA-3-R","MDL-1-R","MDL-10-R","MDL-12-R","MDL-2-R","MDL-4-R","MDL-5-R","MDL-6-R","MDL-8-R","GDL2","OT30","RFS60/RLS60","TR100R","TR10R","TR125R","TR12R","TR17-1/2R","TR1R","TR200R","TR20R","TR35R","TR60R","TRM1-1/4","TRM2","TRM3","TRM4","TRS10R","TRS125R","TRS15R","TRS175R","TRS20R","TRS25R","TRS30R","TRS35R","TRS45R","TRS60R","TRS80R","ATQR25","KTK-20"]

for item in products_to_find_list:
    search_bar = driver.find_element_by_name("q")
    search_bar.send_keys(item)
    searc_bar.send_keys(Keys.RETURN)
    r = requests.get(driver.current_url)
    soup - BeautifulSoup(r.content, 'lxml')