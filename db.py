import sqlite3

__connection = None

def ensure_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0 #res
    return inner()


def ensure_connection_init_db(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0 #res
    return inner()

def ensure_connection_add_film(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0 #res
    return inner()

def ensure_connection_get_list(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('filmlist.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return 0 #res
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
       description  Text  
    )
    ''')
    conn.commit()


def add_film(conn, cinema_id: int, name: str, rating, link: str, description: str):

    c = conn.cursor()
    c.execute('INSERT INTO film (cinema_id, name, rating, link, description) VALUES (?, ?, ?, ?)', (cinema_id, name, rating, link, description))
    conn.commit()


def get_list_of_films(conn, cinema_id: int):

    c = conn.cursor()
    c.execute('SELECT name, rating FROM film WHERE cinema_id = ?', (cinema_id, ))
    return c.fetchall()

def fun1(fun):

    def fun2(*args, **kwargs):
        print(args, kwargs)
        res = fun(*args, **kwargs, nv = 2)
        return res
    return fun2()

def test(nv, a, b):
    print(a+b+nv)


if __name__ == '__main__':
    pass
    #with sqlite3.connect('filmlist.db') as conn:
        #init_db(conn=conn, force=True)
    #with sqlite3.connect('filmlist.db') as conn:
        #add_film(conn=conn, cinema_id=1, name='eferf', rating='42', link='errferf')
    #add_film(cinema_id=1, name='eferf', rating='42', link='errferf')


