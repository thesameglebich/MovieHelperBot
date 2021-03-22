from copy import copy

import requests
from bs4 import BeautifulSoup

URL = "https://www.kinopoisk.ru/index.php?kp_query="
URL2 = "https://www.kinopoisk.ru/film/"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    html = requests.get(url, headers=HEADERS, params=params)
    return html


# second parser for second variant of page
def get_content2(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('div', class_='styles_subRating__VEOSH film-sub-rating')[0]
    #print(item)
    # print(item.get_text())
    return item.get_text()


def parse2(newlink):
    html = get_html(newlink)
    if html.status_code == 200:
        #print(html.text)
        get_content2(html.text)
    else:
        print('Error')


# first

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('div', class_='right')
    if item:
        item = item[0]
        if item.find('div', class_='rating'):
            return item.find('div', class_='rating').get_text()
        else:
            #return 'я пока хз как фиксить'
            print('here')
            link = item.find('ul', class_='links').find_next('li').find_next('a').get('href')
            filmindex = link.split('/')[2]
            newlink = URL2 + filmindex + '/'
            print(newlink)
            return parse2(newlink)
    else:
        return 'error'


def parse_rating(name):
    html = get_html(search_film(name))
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print('Error')


def search_film(name):
    masswords = name.split()
    masswords = masswords[:-1]
    newURl = copy(URL)

    for i in range(len(masswords)):
        newURl += masswords[i] + "+"
    newURl = newURl.replace(',', '')
    print(newURl)
    return newURl


#mystr = "Норм и несокрушимые: Семейные каникулы (6+)"

#parse(mystr)
