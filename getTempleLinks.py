import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Hindu_temples_in_India"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_='mw-parser-output').find_all('ul')

for i, child in enumerate(results):
    if i >= 1 and i <= 34:
        children_li = child.find_all('li')
        for child_li in children_li:
            if child_li.find('a') != None and child_li.find('a').get('href').count('/wiki/'):
                print("https://en.wikipedia.org/" + child_li.find('a').get('href'))