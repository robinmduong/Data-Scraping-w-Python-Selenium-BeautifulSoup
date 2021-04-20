# pip install selenium
import requests
from bs4 import BeautifulSoup

baseurl = 'http://www.allfuses.com'

headers = {
    # CHROME 80 on WINDOWS: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=breadcrumbs
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

productlinks = []

for x in range(1, 2): # Range specifics the page range
    r = requests.get(f'https://www.allfuses.com/all-products?p={x}&product_list_limit=100')
    soup = BeautifulSoup(r.content, 'lxml')# r.content to get everything on the page
    productlist = soup.find_all('li', class_='product-item')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(link['href'])

itemlist = []

for link in productlinks:
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    name_description = soup.find('span', itemprop='name').get_text()
    quick_overview = soup.find('div', itemprop='description').get_text()
    details = soup.find('div', class_='product attribute description')
    # image, weight, info_size_color 
    product = {
        'description': name_description,
        'quick_overview': quick_overview,
        'details': details,
    }

    itemlist.append(product)

print(itemlist)