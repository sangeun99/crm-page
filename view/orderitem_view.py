from flask import Blueprint, request, render_template

from view.common import get_data_from_file, get_pages_indexes, get_results


orderitem_bp = Blueprint('orderitem', __name__)

def find_orderitem_detail(orderitem, orderitem_id):
    for oi in orderitem:
        if oi['id'] == orderitem_id:
            order_info = oi
            return order_info
    return None

@orderitem_bp.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    orderitem = get_data_from_file('src/orderlist.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(orderitem), page)

    return render_template("common/list.html", model="orderitem", data=orderitem[start_index:end_index],
                           total_pages=total_pages, page=page)

@orderitem_bp.route('/orderitem_detail/')
def orderitem_detail():
    orderitem_id = request.args.get('id', default="", type=str)
    
    orderitem = get_data_from_file('src/orderlist.csv')
    orderitem_info = find_orderitem_detail(orderitem, orderitem_id)

    return render_template("common/detail.html", model="orderitem", detail_info=orderitem_info)