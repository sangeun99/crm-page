from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_one, get_all, insert_one
from models.store import Store


store_bp = Blueprint('store', __name__)

@store_bp.route("/stores/")
def stores():
    page = request.args.get('page', default=1, type=int)

    count_query = 'SELECT COUNT(*) FROM stores'
    length = get_all(count_query)[0]['COUNT(*)']

    total_pages, per_page, start_index =  get_pages_indexes(length, page)
    query = 'SELECT * FROM stores'
    query += f" LIMIT {start_index}, {per_page}"
    stores = get_all(query)

    return render_template("common/list.html", model="store", data=stores,
                           total_pages=total_pages, page=page)

@store_bp.route("/store_detail/")
def store_detail():
    store_id = request.args.get('id', default="", type=str)

    store_info = get_one('SELECT * FROM stores WHERE id = ?', store_id)

    return render_template("common/detail.html", model="store", detail_info=store_info)

@store_bp.route("/store/register", methods=['GET', 'POST'])
def store_register():
    if request.method == 'POST':
        get = request.form
        store = Store(get['storetype'], get['storelocation'], get['address']).generate()
        store_tuple = tuple(store.values())

        insert_one("insert into stores values (?, ?, ?, ?)", store_tuple)

        return render_template('register_complete.html', data=store)
    return render_template('store_register.html')