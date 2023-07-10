from flask import Flask, render_template

from test import User

from view.user_view import user_bp
from view.order_view import order_bp
from view.orderitem_view import orderitem_bp
from view.item_view import item_bp
from view.store_view import store_bp
from view.common import get_results

app = Flask(__name__, static_folder="static")


app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)
app.register_blueprint(store_bp)


@app.route('/test')
def test():
    result = get_results("SELECT * FROM users WHERE name = ?", "김아린")

    print(result)
    return "complete1"

@app.route("/")
def root():
    return render_template('home.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)