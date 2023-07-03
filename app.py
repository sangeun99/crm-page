from flask import Flask, render_template, url_for, request
import csv

app = Flask(__name__, static_folder="static")

def get_data_from_file(filename):
    data = []
    with open(filename, newline='', encoding="utf-8") as user:
        reader = csv.DictReader(user, skipinitialspace=True)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def filter_data(data, search_name="", search_gender="", search_age=0):
    filtered_data = []
    highlighted = []
    if bool(search_name) or bool(search_gender) or bool(search_age) : # 검색어가 있다면 데이터 필터링
        for d in data:
            if (is_name_match(search_name, d['Name']) and
                is_gender_match(search_gender, d['Gender']) and
                is_age_match(search_age, int(d['Age']))) :
                filtered_data.append(d)
                match = [0 for _ in range(len(d['Name']))] # match되는 부분을 저장할 list
                if (search_name) :
                    for i in range(len(d['Name'])-len(search_name)+1):
                        if d['Name'][i:i+len(search_name)] == search_name:
                            # match하면 1, 아니면 0으로 남아있음
                            match[i:i+len(search_name)] = [1 for _ in range(i, i+len(search_name))]
                highlighted.append(match)
    else : # 없으면 원래 데이터
        filtered_data = data
    return filtered_data, highlighted

def find_user_detail(users, user_id) :
    for user in users:
        if user['Id'] == user_id :
            user_info = user
            return user_info
    return None
            
def find_store_detail(stores, store_id) :
    for store in stores:
        if store['Id'] == store_id:
            store_info = store
            return store_info
    return None

def find_order_detail(orders, order_id):
    for order in orders:
        if order['Id'] == order_id:
            order_info = order
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
    return render_template('index.html')

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
    user_id = request.args.get('user_id', default="", type=str)

    users = get_data_from_file('src/user.csv')
    user_info = find_user_detail(users, user_id)

    return render_template("user_detail.html", user_info=user_info)

# ============
#   stores
# ============

@app.route("/stores/")
def stores():
    stores = get_data_from_file('src/store.csv')
    return render_template("stores.html", stores=stores)

@app.route("/store_detail/")
def store_detail():
    store_id = request.args.get('store_id', default="", type=str)

    stores = get_data_from_file('src/store.csv')
    store_info = find_store_detail(stores, store_id)

    return render_template("store_detail.html", store_info=store_info)

# ============
#   orders
# ============

@app.route('/orders/')
def orders():
    orders = get_data_from_file('src/order.csv')
    print(orders)
    return render_template("orders.html", orders=orders)

@app.route('/order_detail/')
def order_detail():
    order_id = request.args.get('order_id', default="", type=str)
    
    orders = get_data_from_file('src/order.csv')
    order_info = find_order_detail(orders, order_id)

    return render_template("order_detail.html", order_info=order_info)

if __name__=="__main__":
    app.run(port=8080, debug=True)