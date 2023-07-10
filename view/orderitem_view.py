from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_one_result, get_results


orderitem_bp = Blueprint('orderitem', __name__)

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    orderitem = get_results('SELECT * FROM order_items')
    total_pages, start_index, end_index =  get_pages_indexes(len(orderitem), page)

    return render_template("common/list.html", model="orderitem", data=orderitem[start_index:end_index],
                           total_pages=total_pages, page=page)

@orderitem_bp.route('/orderitem_detail/')
def orderitem_detail():
    orderitem_id = request.args.get('id', default="", type=str)

    orderitem_info = get_one_result('SELECT * FROM order_items WHERE id=?', orderitem_id)

    return render_template("common/detail.html", model="orderitem", detail_info=orderitem_info)