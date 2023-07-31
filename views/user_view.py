from flask import Blueprint, render_template, request
from sqlalchemy import and_
from sqlalchemy import func
import datetime
import uuid

from database.model import db, User, Store, Item, Order, OrderItem


user_bp = Blueprint('user', __name__)

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

def get_age(birthdate) :
    dateToday = datetime.datetime.now()
    if birthdate :
        age = dateToday.year - int(birthdate[:4]) + 1
    return age

def generate_id():
    return str(uuid.uuid4())

@user_bp.route('/users/')
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

@user_bp.route('/user_detail/')
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

@user_bp.route("/user/register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST' :
        get = request.form
        new_user = User(Id=generate_id(), Name=get['name'], Gender=get['gender'], Age=get_age(get['birthdate']), Birthdate=get['birthdate'], Address=get['address'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('register_complete.html', new_data=new_user)
    return render_template('user_register.html')