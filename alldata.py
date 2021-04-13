from db import init_db, get_list_of_films, add_film
from Kinmomax_parser import parse as kinomaxparse
from Goodwin import parseGoodwin
from YouTube import findlink
import sqlite3


def update_data_base():
    with sqlite3.connect('filmlist.db') as conn:
        init_db(conn=conn, force=True)
    kinomaxmas = kinomaxparse()
    goodwinmas = parseGoodwin()
    for i in range(len(kinomaxmas)):
        name = kinomaxmas[i]['title']
        rating = kinomaxmas[i]['rating']
        link = kinomaxmas[i]['link']
        with sqlite3.connect('filmlist.db') as conn:
            add_film(conn=conn,
                     cinema_id=1,
                     name=name,
                     rating=rating,
                     link=link)

    for i in range(len(goodwinmas)):
        name = goodwinmas[i]['title']
        rating = goodwinmas[i]['rating']
        link = goodwinmas[i]['link']
        with sqlite3.connect('filmlist.db') as conn:
            add_film(conn=conn,
                     cinema_id=2,
                     name=name,
                     rating=rating,
                     link=link)
