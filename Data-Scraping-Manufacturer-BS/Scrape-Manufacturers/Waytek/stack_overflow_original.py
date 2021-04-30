# Code provided by the wonderful QHarr on StackOverflow
from bs4 import BeautifulSoup
from selenium import webdriver # links w/ browser and carries out actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
baseurl = "http://www.waytekwire.com"
skus_to_find_test = ['WL16-8', 'WG18-12']

driver = webdriver.Chrome(PATH)
driver.get(baseurl)

def use_driver_current_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup

for sku in skus_to_find_test[0]:
    
    search_bar = driver.find_element_by_id('themeSearchText')
    search_bar.send_keys(sku)
    search_bar.send_keys(Keys.RETURN)   

    try:
        
        product_url = driver.find_elements_by_xpath("//div[contains(@class, 'itemDescription')]//h3//a[contains(text(), sku)]")[0]
        product_url.click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@itemprop, 'description')]")))
        soup = use_driver_current_html(driver)
        
        try:
            quick_overview = soup.select_one("span[itemprop=description]").text
            print(quick_overview)
        except:
            print('No Quick Overview Found.')
            
    except:
        print('Product not found.')