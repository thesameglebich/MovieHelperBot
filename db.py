import sqlite3

__connection = None


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0  # res

    return inner()


def ensure_connection_init_db(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0  # res

    return inner()


def ensure_connection_add_film(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0  # res

    return inner()


def ensure_connection_get_list(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0  # res

    return inner()


def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS film')

    c.execute('''
    CREATE TABLE IF NOT EXISTS film (
       id           INTEGER PRIMARY KEY,
       cinema_id    INTEGER NOT NULL,
       name         TEXT NOT NULL,
       rating       TEXT,
       link         TEXT,
       description  TEXT
    )
    ''')
    conn.commit()


def add_film(conn, cinema_id: int, name: str, rating, link: str, description: str):
    c = conn.cursor()
    c.execute('INSERT INTO film (cinema_id, name, rating, link, description) VALUES (?, ?, ?, ?, ?)', (cinema_id, name, rating, link, description))
    conn.commit()


def get_list_of_films(conn, cinema_id: int):
    c = conn.cursor()
    c.execute('SELECT name, rating, link, description FROM film WHERE cinema_id = ? ORDER BY rating DESC', (cinema_id,))
    mastuple =  c.fetchall()
    newmas = []
    for i in range(len(mastuple)):
        newmas.append(
            {
                'title': mastuple[i][0],
                'rating': mastuple[i][1],
                'link': mastuple[i][2],
                'description': mastuple[i][3]
            }
        )
    return newmas


if __name__ == '__main__':
    with sqlite3.connect('filmlist.db') as conn:
        mylist = get_list_of_films(conn, 1)
        print(mylist)