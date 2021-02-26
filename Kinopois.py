from copy import copy

import requests
from bs4 import BeautifulSoup

URL = "https://www.kinopoisk.ru/index.php?kp_query="

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    html = requests.get(url, headers=HEADERS, params=params)
    return html


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    #items = soup.find_all('div', class_='right')
    items = soup.find_all('div', class_='rating')
    #print(items)
    films = []
    for item in items:
        films.append(
            {
                'title': item.get_text(),
                #'title': item.find('ul').find_next('li', class_='inactive').get_text(strip=True),
                # 'url': URL + item.find('a').get('href')
            }
        )
    print(films)



def parse(name):
    html = get_html(search_film(name))
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')

def search_film(name):
    masswords = name.split()
    masswords = masswords[:-2]
    newURl = copy(URL)

    for i in range(len(masswords)):
        newURl += masswords[i] + "+"
    newURl = newURl.replace(',', '')
    print(newURl)
    return newURl


mystr = "Скайлайн 3 (2D, 16+)"

parse(mystr)

