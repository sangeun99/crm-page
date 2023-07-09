from flask import Blueprint, request, render_template

from view.common import get_data_from_file, get_pages_indexes, get_results, write_csv
from models.item import Item

item_bp = Blueprint('item', __name__)

def find_item_detail(items, item_id):
    for item in items:
        if item['id'] == item_id:
            item_info = item
            return item_info
    return None

@item_bp.route('/items/')
def items():
    page = request.args.get('page', default=1, type=int)

    items = get_data_from_file('src/item.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(items), page)

    return render_template("common/list.html", model="item", data=items[start_index:end_index],
                           total_pages=total_pages, page=page)

@item_bp.route('/item_detail/')
def item_detail():
    item_id = request.args.get('id', default="", type=str)

    items = get_data_from_file('src/item.csv')
    item_info = find_item_detail(items, item_id)

    return render_template("common/detail.html", model="item", detail_info=item_info)

@item_bp.route("/item/register", methods=['GET', 'POST'])
def item_register():
    if request.method == 'POST':
        get = request.form
        item = Item(get['itemname'], get['itemtype'], get['unitprice']).generate()
        fieldnames = ['id', 'name', 'type', 'unitprice']
        write_csv('src/item.csv', fieldnames, item)
        return render_template('register_complete.html', data=item)
    return render_template('item_register.html')
