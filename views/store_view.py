from flask import Blueprint, render_template, request

from sqlalchemy import and_
from sqlalchemy import func
from database.model import db, User, Store, Item, Order, OrderItem


store_bp = Blueprint('store', __name__)

def get_length(model):
    count = db.session.query(func.count(model.Id)) \
        .first()
    return int(count[0])

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    return total_pages, per_page, start_index

@store_bp.route('/stores/')
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

@store_bp.route('/store_detail/')
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

    return render_template("store_detail.html", model="store", detail_info=store_info,
                           sales_per_month_info=sales_per_month_info)
