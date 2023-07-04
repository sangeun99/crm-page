from flask import Flask, render_template, url_for, request
import csv

app = Flask(__name__, static_folder="static")

def get_data_from_file(filename):
    data = []
    with open(filename, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def filter_data(data, search_name="", search_gender="", search_age=0):
    filtered_data = []
    highlighted = []
    if bool(search_name) or bool(search_gender) or bool(search_age) : # 검색어가 있다면 데이터 필터링
        for d in data:
            if (is_name_match(search_name, d['name']) and
                is_gender_match(search_gender, d['gender']) and
                is_age_match(search_age, int(d['age']))) :
                filtered_data.append(d)
                match = [0 for _ in range(len(d['name']))] # match되는 부분을 저장할 list
                if (search_name) :
                    for i in range(len(d['name'])-len(search_name)+1):
                        if d['name'][i:i+len(search_name)] == search_name:
                            # match하면 1, 아니면 0으로 남아있음
                            match[i:i+len(search_name)] = [1 for _ in range(i, i+len(search_name))]
                highlighted.append(match)
    else : # 없으면 원래 데이터
        filtered_data = data
    return filtered_data, highlighted

def find_user_detail(users, user_id) :
    for user in users:
        if user['id'] == user_id :
            user_info = user
            return user_info
    return None
            
def find_store_detail(stores, store_id) :
    for store in stores:
        if store['id'] == store_id:
            store_info = store
            return store_info
    return None

def find_order_detail(orders, order_id):
    for order in orders:
        if order['id'] == order_id:
            order_info = order
            return order_info
    return None

def find_orderitem_detail(orderitem, orderitem_id):
    for oi in orderitem:
        if oi['id'] == orderitem_id:
            order_info = oi
            return order_info
    return None

def is_name_match(search_name, data_name):
    if (search_name in data_name) :
        return True
    return False

def is_gender_match(search_gender, data_gender):
    if not search_gender:
        return True
    elif (search_gender.lower() == data_gender.lower()):
        return True
    return False

def is_age_match(search_age, data_age):
    if search_age == 0:
        return True
    elif data_age // 10 * 10 == search_age :
        return True
    else :
        return False

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = data_length // per_page + 1
    start_index = (page - 1) * per_page
    end_index = page * per_page
    return total_pages, start_index, end_index

@app.route("/")
def root():
    return render_template('home.html')

# ============
#   users
# ============

@app.route("/users/")
def users():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default="", type=str)
    search_gender = request.args.get('gender', default="", type=str)
    search_age = request.args.get('age', default=0, type=int)

    data = get_data_from_file('src/user.csv') # 데이터 불러오기
    final_data, highlighted = filter_data(data, search_name, search_gender, search_age)
    total_pages, start_index, end_index =  get_pages_indexes(len(final_data), page)

    return render_template("users.html", users=final_data[start_index:end_index], highlighted=highlighted[start_index:end_index],
                           total_pages=total_pages, page=page, 
                           search_name=search_name, search_gender= search_gender, search_age = search_age)

@app.route("/user_detail/")
def user_detail():
    user_id = request.args.get('id', default="", type=str)

    users = get_data_from_file('src/user.csv')
    user_info = find_user_detail(users, user_id)

    print("user",user_info)
    return render_template("common/detail.html", model="user", detail_info=user_info)

# ============
#   stores
# ============

@app.route("/stores/")
def stores():
    page = request.args.get('page', default=1, type=int)

    stores = get_data_from_file('src/store.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(stores), page)

    return render_template("common/list.html", model="store", data=stores[start_index:end_index],
                           total_pages=total_pages, page=page)

@app.route("/store_detail/")
def store_detail():
    store_id = request.args.get('id', default="", type=str)

    stores = get_data_from_file('src/store.csv')
    store_info = find_store_detail(stores, store_id)

    return render_template("common/detail.html", model="store", detail_info=store_info)

# ============
#   orders
# ============

@app.route('/orders/')
def orders():
    page = request.args.get('page', default=1, type=int)

    orders = get_data_from_file('src/order.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(orders), page)

    return render_template("common/list.html", model="order", data=orders[start_index:end_index],
                           total_pages=total_pages, page=page)

@app.route('/order_detail/')
def order_detail():
    order_id = request.args.get('id', default="", type=str)
    
    orders = get_data_from_file('src/order.csv')
    order_info = find_order_detail(orders, order_id)

    return render_template("common/detail.html", model="order", detail_info=order_info)


# ============
#  orderitems
# ============

@app.route('/orderitem/')
def orderitem():
    page = request.args.get('page', default=1, type=int)

    orderitem = get_data_from_file('src/orderlist.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(orderitem), page)

    return render_template("common/list.html", model="orderitem", data=orderitem[start_index:end_index],
                           total_pages=total_pages, page=page)

@app.route('/orderitem_detail/')
def orderitem_detail():
    orderitem_id = request.args.get('id', default="", type=str)
    
    orderitem = get_data_from_file('src/orderlist.csv')
    orderitem_info = find_orderitem_detail(orderitem, orderitem_id)

    return render_template("common/detail.html", model="orderitem", detail_info=orderitem_info)

# ============
#   items
# ============
@app.route('/items/')
def items():
    page = request.args.get('page', default=1, type=int)

    items = get_data_from_file('src/item.csv')
    total_pages, start_index, end_index =  get_pages_indexes(len(items), page)

    return render_template("common/list.html", model="item", data=items[start_index:end_index],
                           total_pages=total_pages, page=page)

@app.route('/item_detail/')
def item_detail():
    item_id = request.args.get('id', default="", type=str)

    items = get_data_from_file('src/item.csv')
    item_info = find_order_detail(items, item_id)

    return render_template("common/detail.html", model="item", detail_info=item_info)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)