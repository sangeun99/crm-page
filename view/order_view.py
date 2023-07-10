from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_results, get_one_result


order_bp = Blueprint('order', __name__)

@order_bp.route('/orders/')
def orders():
    page = request.args.get('page', default=1, type=int)

    orders = get_results('SELECT * FROM orders')
    total_pages, start_index, end_index =  get_pages_indexes(len(orders), page)

    return render_template("common/list.html", model="order", data=orders[start_index:end_index],
                           total_pages=total_pages, page=page)

@order_bp.route('/order_detail/')
def order_detail():
    order_id = request.args.get('id', default="", type=str)
    
    order_info = get_one_result('SELECT * FROM orders WHERE id=?', order_id)

    return render_template("common/detail.html", model="order", detail_info=order_info)
