from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_one, get_all, insert_one
from models.item import Item


item_bp = Blueprint('item', __name__)

@item_bp.route('/items/')
def items():
    page = request.args.get('page', default=1, type=int)

    count_query = 'SELECT COUNT(*) FROM items'
    length = get_all(count_query)[0]['COUNT(*)']

    total_pages, per_page, start_index = get_pages_indexes(length, page)

    query = 'SELECT * FROM items'
    query += f" LIMIT {start_index}, {per_page}"
    items = get_all(query)

    return render_template("common/list.html", model="item", data=items,
                           total_pages=total_pages, page=page)

@item_bp.route('/item_detail/')
def item_detail():
    item_id = request.args.get('id', default="", type=str)

    item_info = get_one('SELECT * FROM items WHERE id=?', item_id)

    return render_template("common/detail.html", model="item", detail_info=item_info)

@item_bp.route("/item/register", methods=['GET', 'POST'])
def item_register():
    if request.method == 'POST':
        get = request.form
        item = Item(get['itemname'], get['itemtype'], get['unitprice']).generate()

        item_tuple = tuple(item.values())

        insert_one("insert into items values (?, ?, ?, ?)", item_tuple)

        return render_template('register_complete.html', data=item)
    return render_template('item_register.html')
