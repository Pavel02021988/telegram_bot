import sqlite3


# декоратор для подключения к бд
def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('anketa.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    return inner
@ ensure_connection
def init_db(conn, force: bool=False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS user_message')
    c.execute(''' CREATE TABLE IF NOT EXISTS user_message (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL) ''')
    conn.commit()

# добавление сообщений в бд
@ensure_connection
def add_message(conn, user_id, text):
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()

# подсчет сообщений в бд
@ensure_connection
def count_messages(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_message WHERE user_id = ?', (user_id, ))
    (res, ) = c.fetchone()
    return res

# показать определенное колличество сообщений из бд
@ensure_connection
def list_messages(conn, user_id, limit):
    c = conn.cursor()
    c.execute('SELECT id, text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ? ', (user_id, limit))
    return c.fetchall()
