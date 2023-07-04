from flask import Blueprint, request, render_template
from common import get_data_from_file, get_pages_indexes

store_bp = Blueprint('store', __name__)
            
def find_store_detail(stores, store_id) :
    for store in stores:
        if store['id'] == store_id:
            store_info = store
            return store_info
    return None

@store_bp.route("/stores/")
def stores():
    page = request.args.get('page', default=1, type=int)

    stores = get_data_from_file('src/store.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(stores), page)

    return render_template("common/list.html", model="store", data=stores[start_index:end_index],
                           total_pages=total_pages, page=page)

@store_bp.route("/store_detail/")
def store_detail():
    store_id = request.args.get('id', default="", type=str)

    stores = get_data_from_file('src/store.csv')
    store_info = find_store_detail(stores, store_id)

    return render_template("common/detail.html", model="store", detail_info=store_info)