from flask import Flask, render_template, request
from user import user_bp
from order import order_bp
from orderitem import orderitem_bp
from item import item_bp
from store import store_bp

from models.user import User

import csv

app = Flask(__name__, static_folder="static")

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)
app.register_blueprint(store_bp)

@app.route("/")
def root():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        get = request.form
        user = User(get['name'], get['gender'], get['birthdate'], get['address']).generate()

        filename = 'src/user.csv'
        with open(filename, 'a', newline='', encoding="utf-8") as file:
            fieldnames = ['id', 'name', 'gender', 'age', 'birthdate', 'address']
            writer = csv.DictWriter(file, skipinitialspace=True, fieldnames=fieldnames)
            writer.writerow(user)
        return render_template('register_complete.html', user=user)
    return render_template('register.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)