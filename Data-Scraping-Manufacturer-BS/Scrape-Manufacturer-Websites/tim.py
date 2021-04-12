# pip install selenium
from selenium import webdriver # links up with browser and performs actions
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# FOR CHROME
PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# FOR FIREFOX
# PATH = "C:\Program Files (x86)\geckodriver_v0.29.1_win64\geckodriver.exe"
# driver = webdriver.Firefox(executable_path=PATH)

baseurl = "http://www.allfuses.com"
driver.get("http://www.allfuses.com/all-products")

product_details_link = driver.find_element_by_class_name("product.item.link")
product_details_link.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME(ITEMPROP="name")))
    )
    print(element)
finally:
    driver.quit()

# product_list = ["FRN-R-20", "FLNR-009", "ATQ-20"]

# for item in product_list:
#     search_bar = driver.find_element_by_name("q")
#     search_bar.send_keys(item)
#     search_bar.send_keys(Keys.RETURN)
    # time.sleep(5)

    # try:
    #     main = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "main"))
    #     )
    #     print(main.text)

    #     product_name = main.find_elements_by_class_name("base")
    #     print(product_name)
    # except:
    #     driver.quit()

# print(driver.page_source)