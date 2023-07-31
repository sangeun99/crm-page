import os
from flask import Flask, render_template

from database.model import db
from views.user_view import user_bp
from views.store_view import store_bp
from views.item_view import item_bp
from views.order_view import order_bp


app = Flask(__name__)

app.instance_path = os.path.join(os.getcwd(), 'src')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-sample.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFIATIONS'] = False
app.debug = True

# ===================
#   DB 모델 정의
# ===================

db.init_app(app)

# ===================
#       view
# ===================

app.register_blueprint(user_bp)
app.register_blueprint(store_bp)
app.register_blueprint(item_bp)
app.register_blueprint(order_bp)

@app.route('/')
def main():
    return render_template('home.html')

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run()