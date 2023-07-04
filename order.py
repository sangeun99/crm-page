from flask import Blueprint, request, render_template
from common import get_data_from_file, get_pages_indexes

order_bp = Blueprint('order', __name__)

def find_order_detail(orders, order_id):
    for order in orders:
        if order['id'] == order_id:
            order_info = order
            return order_info
    return None

@order_bp.route('/orders/')
def orders():
    page = request.args.get('page', default=1, type=int)

    orders = get_data_from_file('src/order.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(orders), page)

    return render_template("common/list.html", model="order", data=orders[start_index:end_index],
                           total_pages=total_pages, page=page)

@order_bp.route('/order_detail/')
def order_detail():
    order_id = request.args.get('id', default="", type=str)
    
    orders = get_data_from_file('src/order.csv')
    order_info = find_order_detail(orders, order_id)

    return render_template("common/detail.html", model="order", detail_info=order_info)
