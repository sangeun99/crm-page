from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_one, get_all


orderitem_bp = Blueprint('orderitem', __name__)

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    count_query = 'SELECT COUNT(*) FROM order_items'
    length = get_all(count_query)[0]['COUNT(*)']

    total_pages, per_page, start_index =  get_pages_indexes(length, page)
    query = 'SELECT * FROM order_items'
    query += f" LIMIT {start_index}, {per_page}"
    print(query)
    orderitem = get_all(query)

    return render_template("common/list.html", model="orderitem", data=orderitem,
                           total_pages=total_pages, page=page)

@orderitem_bp.route('/orderitem_detail/')
def orderitem_detail():
    orderitem_id = request.args.get('id', default="", type=str)

    orderitem_info = get_one('SELECT * FROM order_items WHERE id=?', orderitem_id)

    return render_template("common/detail.html", model="orderitem", detail_info=orderitem_info)