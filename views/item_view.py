from flask import Blueprint, render_template, request

from sqlalchemy import and_
from sqlalchemy import func
from database.model import db, User, Store, Item, Order, OrderItem


item_bp = Blueprint('item', __name__)

def get_length(model):
    count = db.session.query(func.count(model.Id)) \
        .first()
    return int(count[0])

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    return total_pages, per_page, start_index

@item_bp.route('/items/')
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

@item_bp.route('/item_detail/')
def item_detail():
    item_id = request.args.get('id', default=1, type=str)

    item_info = Item.query.filter_by(Id=item_id).first()

    return render_template("item_detail.html", model="item", detail_info=item_info)
