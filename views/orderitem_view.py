from flask import Blueprint, render_template, request

from sqlalchemy import and_
from sqlalchemy import func
from database.model import db, User, Store, Item, Order, OrderItem


orderitem_bp = Blueprint('orderitem', __name__)

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    return total_pages, per_page, start_index

def get_length(model):
    count = db.session.query(func.count(model.Id)) \
        .first()
    return int(count[0])

@orderitem_bp.route('/orderitems/')
def orderitems():
    page = request.args.get('page', default=1, type=int)

    length = get_length(OrderItem)
    total_pages, per_page, start_index = get_pages_indexes(length, page)

    orderitems = OrderItem.query \
        .offset(start_index) \
        .limit(per_page) \
        .all()
    
    header = ['Id', 'OrderId', 'ItemId']
    return render_template("orderitems.html", data=orderitems,
                           total_pages=total_pages, page=page, header=header)

@orderitem_bp.route('/orderitem_detail/')
def orderitem_detail():
    orderitem_id = request.args.get('id', default="", type=str)
    
    orderitem_info = OrderItem.query.filter_by(Id=orderitem_id).first()

    return render_template("orderitem_detail.html", model="order", detail_info=orderitem_info)