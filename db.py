import sqlite3

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('filmlist.db')
    return __connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS film')

    c.execute('''
    CREATE TABLE IF NOT EXISTS film (
       id           INTEGER PRIMARY KEY,
       cinema_id    INTEGER NOT NULL,
       name         TEXT NOT NULL,
       rating       DOUBLE 
    )
    ''')
    conn.commit()


def add_film(cinema_id: int, name: str, rating):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO film (cinema_id, name, rating) VALUES (?, ?, ?)', (cinema_id, name, rating))
    get_connection().commit()

def get_list_of_films(cinema_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT name, rating FROM film WHERE cinema_id = ?', (cinema_id, ))
    return c.fetchall()

if __name__ == '__main__':
    init_db(force=True)
    add_film(cinema_id=1, name='майор гром (16+)', rating=12.3)
    add_film(cinema_id=1, name='майор гром 2 (16+)', rating=5.0)

    print(get_list_of_films(1))
