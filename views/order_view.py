from flask import Blueprint, render_template, request

from sqlalchemy import and_
from sqlalchemy import func
from database.model import db, User, Store, Item, Order, OrderItem


order_bp = Blueprint('order', __name__)

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    return total_pages, per_page, start_index

def get_length(model):
    count = db.session.query(func.count(model.Id)) \
        .first()
    return int(count[0])

@order_bp.route('/orders/')
def orders():
    page = request.args.get('page', default=1, type=int)

    length = get_length(Order)
    total_pages, per_page, start_index = get_pages_indexes(length, page)
    
    orders = Order.query \
        .offset(start_index) \
        .limit(per_page) \
        .all()

    header = ['Id', 'OrderAt', 'StoreId', 'UserId']
    return render_template("orders.html", data=orders,
                           total_pages=total_pages, page=page, header=header)

@order_bp.route('/order_detail/')
def order_detail():
    order_id = request.args.get('id', default="", type=str)
    
    order_info = Order.query.filter_by(Id=order_id).first()

    return render_template("order_detail.html", model="order", detail_info=order_info)
