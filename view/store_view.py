from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_one_result, get_results, write_csv
from models.store import Store


store_bp = Blueprint('store', __name__)

@store_bp.route("/stores/")
def stores():
    page = request.args.get('page', default=1, type=int)

    stores = get_results('SELECT * FROM stores')
    total_pages, start_index, end_index =  get_pages_indexes(len(stores), page)

    return render_template("common/list.html", model="store", data=stores[start_index:end_index],
                           total_pages=total_pages, page=page)

@store_bp.route("/store_detail/")
def store_detail():
    store_id = request.args.get('id', default="", type=str)

    store_info = get_one_result('SELECT * FROM stores WHERE id = ?', store_id)

    return render_template("common/detail.html", model="store", detail_info=store_info)

@store_bp.route("/store/register", methods=['GET', 'POST'])
def store_register():
    if request.method == 'POST':
        get = request.form
        store = Store(get['storetype'], get['storelocation'], get['address']).generate()
        fieldnames = ['id', 'name', 'type', 'address']
        write_csv('src/store.csv', fieldnames, store)
        return render_template('register_complete.html', data=store)
    return render_template('store_register.html')
