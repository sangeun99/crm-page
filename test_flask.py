from flask import Flask, render_template
import sqlite3

from test import User


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

@app.route('/test')
def test():
    result = get_results("select * from users")
    # result = get_results("select * from users where name = ?", ["김아린"])
    users = []
    for row in result :
        user = User(row['name'], row['gender'], row['birthdate'], row['address'], row['id']).generate()
        users.append(user)
    return render_template('test.html', result=users)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5000, debug=True)