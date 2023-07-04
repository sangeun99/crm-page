from flask import Flask, render_template
from user import user_bp
from order import order_bp
from orderitem import orderitem_bp
from item import item_bp
from store import store_bp

app = Flask(__name__, static_folder="static")

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(orderitem_bp)
app.register_blueprint(item_bp)
app.register_blueprint(store_bp)

@app.route("/")
def root():
    return render_template('home.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)