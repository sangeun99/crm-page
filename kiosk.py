from flask import Flask, request, render_template

from view.common import get_pages_indexes, get_one, get_all, insert_one, get_length
from models.user import User
from models.order import Order
from models.orderitem import Orderlist

app = Flask(__name__, static_folder="static")

@app.route("/", methods=['GET', 'POST'])
def root():
    return render_template('home.html')

@app.route("/kiosk/", methods=['GET', 'POST'])
def select_store():

    query = 'SELECT * FROM stores'
    stores = get_all(query)

    if request.method == 'POST':
        get = request.form
        store = get_one("SELECT * FROM stores where id=?", get['storeid'])
        query = 'SELECT * FROM items'
        items = get_all(query)

        return render_template('kiosk_item.html', data=items, store_info=store)

    return render_template('kiosk_store.html', data=stores)

@app.route("/kiosk/order/", methods=['GET', 'POST'])
def select_item():

    if request.method == 'POST':
        get = request.form
        print(get)
        # user = User("", "", "", "").generate()
        # user_tuple = tuple(user.values())
        # order = Order(get['storeid'], user['id']).generate()
        # order_tuple = tuple(order.values())
        # insert_one("insert into users values (?, ?, ?, ?, ?, ?)", user_tuple)
        # insert_one("insert into orders values (?, ?, ?, ?)", order_tuple)
        # orderitem = Orderlist(order['orderid'], get['itemid']).generate()
        # orderitem_tuple = tuple(orderitem.values())
        # insert_one("insert into order_items values (?, ?, ?)", orderitem_tuple)

        # return render_template('order_complete.html',
        #                        user_info=user, order_info=order, orderitem_info=orderitem)
        return render_template('home.html')
    return render_template('home.html')

    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)