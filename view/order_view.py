from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_all, get_one


order_bp = Blueprint('order', __name__)

@order_bp.route('/orders/')
def orders():
    page = request.args.get('page', default=1, type=int)

    count_query = 'SELECT COUNT(*) FROM orders'
    length = get_all(count_query)[0]['COUNT(*)']

    total_pages, per_page, start_index = get_pages_indexes(length, page)
    query = 'SELECT * FROM orders'
    query += f" LIMIT {start_index}, {per_page}"
    orders = get_all(query)

    return render_template("common/list.html", model="order", data=orders,
                           total_pages=total_pages, page=page)

@order_bp.route('/order_detail/')
def order_detail():
    order_id = request.args.get('id', default="", type=str)
    
    order_info = get_one('SELECT * FROM orders WHERE id=?', order_id)

    return render_template("common/detail.html", model="order", detail_info=order_info)
