from flask import Flask, g
import sqlite3

app = Flask(__name__)

DATABASE = 'src/user-sample.sqlite'

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_one(query, option=""):
    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()
    if option :
        cur.execute(query, [option])
    else :
        cur.execure(query)
    
    keys = [column[0] for column in cur.description]
    value = cur.fetchone()

    data = dict(zip(keys, value))

    return data

def get_all(query, option="") :
    conn = sqlite3.connect(DATABASE)
    # conn.row_factory = sqlite3.Row # 결과를 딕셔너리처럼 사용 가능

    cur = conn.cursor()
    if option :
        cur.execute(query, option)
    else :
        cur.execute(query)
    
    keys = [column[0] for column in cur.description]
    values = cur.fetchall() # 레코드 단위로 데이터를 전달받음

    data = [dict(zip(keys, value)) for value in values]

    return data

def insert_one(query, option="") :
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query, option)
    conn.commit()

def insert_all(query, option=""):
    pass

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    return total_pages, per_page, start_index