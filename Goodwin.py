import requests
from bs4 import BeautifulSoup
from Kinopois import parse_rating
from YouTube import findlink

URL = "https://goodwincinema.ru/affiche/"
HEADERS = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    'accept': "*/*"}


def get_html(url, params=None):
    html = requests.get(url, headers=HEADERS, params=params)
    return html


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='film-title')
    films = []
    for item in items:
        filmname = item.find('a').get_text(strip=True)
        films.append(
            {
                'title': filmname,
                'rating': parse_rating(filmname),
                'link': findlink(filmname)
            }
        )
        #films[:-1]['rating'] = parse_rating(films[:-1]['title'])
    return films


def parseGoodwin():
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print('Error')

