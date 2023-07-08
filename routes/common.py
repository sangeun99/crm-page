from flask import Flask
import sqlite3
import csv


app = Flask(__name__)

DATABASE = 'user-sample.sqlite'

def get_results(query, option="") :
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # 결과를 딕셔너리처럼 사용 가능

    cur = conn.cursor()
    cur.execute(query, option)

    rows = cur.fetchall() # 레코드 단위로 데이터를 전달받음
    conn.close()
    return rows

def get_data_from_file(filename):
    data = []
    with open(filename, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    end_index = page * per_page
    return total_pages, start_index, end_index
