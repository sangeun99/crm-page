from flask import Blueprint, request, render_template

from view.common import get_pages_indexes, get_one, get_all, insert_one, get_length
from models.store import Store


store_bp = Blueprint('store', __name__)

@store_bp.route("/stores/")
def stores():
    page = request.args.get('page', default=1, type=int)

    length = get_length("stores")

    total_pages, per_page, start_index = get_pages_indexes(length, page)
    query = 'SELECT * FROM stores'
    query += f" LIMIT {start_index}, {per_page}"
    stores = get_all(query)

    sales_per_month_query = """SELECT substr(O.orderat, 0, 8) AS "Month", sum(I.unitprice) AS "Total Revenue", count(I.Id) AS "Item Count"
    FROM stores S
    JOIN orders O on O.storeid = S.Id
    JOIN order_items OI on O.Id = OI.orderid
    JOIN items I on OI.itemid = I.Id
    GROUP BY substr(O.orderat, 0, 8);"""
    sales_per_month = get_all(sales_per_month_query)

    return render_template("stores.html", model="store", data=stores,
                           total_pages=total_pages, page=page, sales_per_month=sales_per_month)

@store_bp.route("/store_detail/")
def store_detail():
    store_id = request.args.get('id', default="", type=str)

    store_info = get_one('SELECT * FROM stores WHERE id = ?', store_id)

    sales_per_month_query = f"""SELECT substr(O.orderat, 0, 8) AS "month", sum(I.unitprice) AS "total_revenue", count(I.Id) AS "item_count"
    FROM stores S
    JOIN orders O on O.storeid = S.Id
    JOIN order_items OI on O.Id = OI.orderid
    JOIN items I on OI.itemid = I.Id
    WHERE S.Id = "{store_id}"
    GROUP BY substr(O.orderat, 0, 8);"""
    sales_per_month = get_all(sales_per_month_query)
    
    labels = []
    total_revenues = []
    item_counts = []
    for month_revenue in sales_per_month:
        labels.append(month_revenue['month'])
        total_revenues.append(month_revenue['total_revenue'])
        item_counts.append(month_revenue['item_count'])


    return render_template("common/detail.html", model="store", detail_info=store_info,
                           sales_per_month=sales_per_month,
                           labels=labels, total_revenues=total_revenues, item_counts=item_counts)

@store_bp.route("/store/register", methods=['GET', 'POST'])
def store_register():
    if request.method == 'POST':
        get = request.form
        store = Store(get['storetype'], get['storelocation'], get['address']).generate()
        store_tuple = tuple(store.values())

        insert_one("insert into stores values (?, ?, ?, ?)", store_tuple)

        return render_template('register_complete.html', data=store)
    return render_template('store_register.html')