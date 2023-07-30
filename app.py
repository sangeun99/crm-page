from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy import func
import os

app = Flask(__name__)

app.instance_path = os.path.join(os.getcwd(), 'src')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-sample.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFIATIONS'] = False
app.debug = True
db = SQLAlchemy(app)

# ===================
#   DB 모델 정의
# ===================

class User(db.Model):
    __tablename__ = 'users'
    Id = db.Column(db.String(64), primary_key=True)
    Name = db.Column(db.String(16))
    Gender = db.Column(db.String(16))
    Age = db.Column(db.Integer())
    Birthdate = db.Column(db.String(32))
    Address = db.Column(db.String(64))
    OrderR = db.relationship('Order', backref='users')

    def __repr__(self): # 파이썬 내장함수
        return f'<User {self.Id}, {self.Name}, {self.Gender}, {self.Age}, {self.Address}>'

class Store(db.Model):
    __tablename__ = 'stores'
    Id = db.Column(db.String(64), primary_key=True)
    Name = db.Column(db.String(32))
    Type = db.Column(db.String(32))
    Address = db.Column(db.String(64))
    OrderR = db.relationship('Order', backref='stores')

    def __repr__(self):
        return f'<Store {self.Id}, {self.Name}, {self.Type}, {self.Address}>'

class Item(db.Model):
    __tablename__ = 'items'
    Id = db.Column(db.String(64), primary_key=True)
    Name = db.Column(db.String(32))
    Type = db.Column(db.String(16))
    UnitPrice = db.Column(db.Integer())
    OrderItemR = db.relationship('OrderItem', backref='items')

    def __repr__(self):
        return f'<Item {self.Id}, {self.Name}, {self.Type}, {self.UnitPrice}>'

class Order(db.Model):
    __tablename__ = 'orders'
    Id = db.Column(db.String(64), primary_key=True)
    OrderAt = db.Column(db.String(64))
    StoreId = db.Column(db.String(64), db.ForeignKey('stores.Id'))
    UserId = db.Column(db.String(64), db.ForeignKey('users.Id'))
    OrderItemR = db.relationship('OrderItem', backref="orders")

    def __repr__(self):
        return f'<Order {self.Id}, {self.OrderAt}, {self.StoreId}, {self.UserId}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    Id = db.Column(db.String(64), primary_key=True)
    OrderId = db.Column(db.String(64), db.ForeignKey('orders.Id'))
    ItemId = db.Column(db.String(64), db.ForeignKey('items.Id'))

    def __repr__(self):
        return f'<OrderItem {self.Id}, {self.OrderId}, {self.ItemId}>'

# ===================
#       view
# ===================

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    return total_pages, per_page, start_index

def get_length_users(search_name, search_gender, search_age) :
    users_count = db.session.query(func.count(User.Id)) \
        .filter(User.Name.like('%'+search_name+'%')) \
        .filter(User.Gender.like(search_gender+'%'))\
        .filter(and_(search_age < User.Age, User.Age < search_age + 9)) \
        .first()
    return int(users_count[0])

def get_length(model):
    count = db.session.query(func.count(model.Id)) \
        .first()
    return int(count[0])

@app.route('/')
def main():
    return 'hello'

@app.route('/users/')
def users():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    search_gender = request.args.get('gender', default='', type=str)
    search_age = request.args.get('age', default=0, type=int)

    length = get_length_users(search_name, search_gender, search_age)
    total_pages, per_page, start_index = get_pages_indexes(length, page)

    users = User.query \
        .filter(User.Name.like('%'+search_name+'%')) \
        .filter(User.Gender.like(search_gender+'%')) \
        .filter(and_(search_age < User.Age, User.Age < search_age + 9)) \
        .offset(start_index) \
        .limit(per_page) \
        .all()

    header = ['Id', 'Name', 'Gender', 'Age', 'Birthdate', 'Address']
    return render_template("users.html", users=users,
                           total_pages=total_pages, page=page, header=header,
                           search_name=search_name, search_gender=search_gender, search_age=search_age)

@app.route('/user_detail/')
def user_detail():
    user_id = request.args.get('id', default="", type=str)

    user_info = User.query.filter_by(Id=user_id).first()

    # user_purchased_info
    user_purchased_info = db.session.query(User.Name.label("username"), Order.Id.label("orderid"), Order.OrderAt.label("orderat"), Store.Name.label("storename")) \
        .join(Order, Order.UserId == User.Id) \
        .join(Store, Store.Id == Order.StoreId) \
        .filter(User.Id == user_id) \
        .all()

    # user_top_store_info
    user_top_store_info = db.session.query(User.Name.label("username"), Store.Name.label("storename"), func.count(Order.Id).label("count_visited")) \
        .join(Order, Order.UserId == User.Id) \
        .join(Store, Store.Id == Order.StoreId) \
        .group_by(Store.Id) \
        .order_by(func.count(Order.Id).desc()) \
        .filter(User.Id == user_id) \
        .limit(5) \
        .all()

    # user_top_item_info
    user_top_item_info = db.session.query(User.Name.label("username"), Item.Name.label("itemname"), func.count(Order.Id).label("count_ordered")) \
        .join(Order, User.Id == Order.UserId) \
        .join(OrderItem, Order.Id == OrderItem.OrderId) \
        .join(Item, Item.Id == OrderItem.ItemId) \
        .group_by(Item.Id) \
        .order_by(func.count(Order.Id).desc()) \
        .filter(User.Id == user_id) \
        .limit(5) \
        .all()

    return render_template("user_detail.html", model="user", detail_info=user_info,
                           purchased_info=user_purchased_info, top_store=user_top_store_info, top_item=user_top_item_info)

@app.route('/stores/')
def stores():
    page = request.args.get('page', default=1, type=int)

    length = get_length(Store)
    total_pages, per_page, start_index = get_pages_indexes(length, page)

    stores = Store.query \
        .offset(start_index) \
        .limit(per_page) \
        .all()
    
    header = ['Id', 'Name', 'Type', 'Address']
    return render_template("stores.html", stores=stores,
                           total_pages=total_pages, page=page, header=header)

@app.route('/store_detail/')
def store_detail():
    store_id = request.args.get('id', default="", type=str)

    store_info = Store.query.filter_by(Id=store_id).first()

    # sales_per_month_info
    sales_per_month_info = db.session.query(Store.Name.label("storename"), func.substr(Order.OrderAt, 0, 8).label("month"), func.sum(Item.UnitPrice).label("total_revenue"), func.count(Item.Id).label("item_count")) \
        .join(Order, Order.StoreId == Store.Id) \
        .join(OrderItem, Order.Id == OrderItem.OrderId) \
        .join(Item, Item.Id == OrderItem.ItemId) \
        .filter(Store.Id == store_id) \
        .group_by(func.substr(Order.OrderAt, 0, 8)) \
        .all()
    print(sales_per_month_info)

    return render_template("store_detail.html", model="store", detail_info=store_info,
                           sales_per_month_info=sales_per_month_info)

@app.route('/item_detail/')
def item_detail():
    item_id = request.args.get('id', default=1, type=str)

    item_info = Item.query.filter_by(Id=item_id).first()

    return render_template("item_detail.html", model="item", detail_info=item_info)
    
@app.route('/items/')
def items():
    page = request.args.get('page', default=1, type=int)

    length = get_length(Item)
    total_pages, per_page, start_index = get_pages_indexes(length, page)

    items = Item.query \
        .offset(start_index) \
        .limit(per_page) \
        .all()
    
    header = ['Id', 'Name', 'Type', 'UnitPrice']
    return render_template("items.html", items=items,
                           total_pages=total_pages, page=page, header=header)
