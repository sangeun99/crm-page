import csv
from flask import Flask, render_template, request

from routes.user import user_bp
from routes.order import order_bp
from routes.orderitem import orderitem_bp
from routes.item import item_bp
from routes.store import store_bp
# from common import get_results

from models.user import User
from models.store import Store
from models.item import Item


app = Flask(__name__, static_folder="static")

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)
app.register_blueprint(store_bp)

# @app.route('/test')
# def root():
#     result = get_results("select * from users")
#     # result = get_results("select * from users where name = ?", ["김아린"])
#     for row in result :
#         print(row['id'])
#         print(row['name'], 'has id', row['id'])
#     return "complete"

@app.route("/")
def root():
    return render_template('home.html')

def write_csv(filename, fieldnames, data) :
    with open(filename, 'a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, skipinitialspace=True, fieldnames=fieldnames)
            writer.writerow(data)

@app.route("/register/user", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        get = request.form
        user = User(get['name'], get['gender'], get['birthdate'], get['address']).generate()
        fieldnames = ['id', 'name', 'gender', 'age', 'birthdate', 'address']
        write_csv('src/user.csv', fieldnames, user)
        return render_template('register_complete.html', data=user)
    return render_template('user_register.html')

@app.route("/register/store", methods=['GET', 'POST'])
def store_register():
    if request.method == 'POST':
        get = request.form
        store = Store(get['storetype'], get['storelocation'], get['address']).generate()
        fieldnames = ['id', 'name', 'type', 'address']
        write_csv('src/store.csv', fieldnames, store)
        return render_template('register_complete.html', data=store)
    return render_template('store_register.html')

@app.route("/register/item", methods=['GET', 'POST'])
def item_register():
    if request.method == 'POST':
        get = request.form
        item = Item(get['itemname'], get['itemtype'], get['unitprice']).generate()
        fieldnames = ['id', 'name', 'type', 'unitprice']
        write_csv('src/item.csv', fieldnames, item)
        return render_template('register_complete.html', data=item)
    return render_template('item_register.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)