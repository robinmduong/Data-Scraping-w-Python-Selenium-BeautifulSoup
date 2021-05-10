from bs4 import BeautifulSoup
import requests

url = "https://www.48ws.com/products/categories/"

page = requests.get(url)    
data = page.text
soup = BeautifulSoup(data, features='lxml')

lines_seen = []


def print_link(url):
    for link in soup.find_all('a'):
        line = link.get('href')
        print(line)
    if line not in lines_seen:
        lines_seen.append(line)
        print_link(line)

print(print_link(page))

with open('category-urls.txt', 'w') as f:
    for item in lines_seen:
        f.write(item)
    # f.close()
    f.flush()