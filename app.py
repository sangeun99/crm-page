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

def filter_data(data, search_name="", search_gender=""):
    filtered_data = []
    highlighted = []
    for d in data:
        if (is_name_match(search_name, d['Name']) and
            is_gender_match(search_gender, d['Gender'])) :
            filtered_data.append(d)
            match = [0 for _ in range(len(d['Name']))] # match되는 부분을 저장할 list
            if (search_name) :
                for i in range(len(d['Name'])-len(search_name)+1):
                    if d['Name'][i:i+len(search_name)] == search_name:
                        # match하면 1, 아니면 0으로 남아있음
                        match[i:i+len(search_name)] = [1 for _ in range(i, i+len(search_name))]
            highlighted.append(match)
    return filtered_data, highlighted

def is_name_match(search_name, data_name):
    if (search_name in data_name) :
        return True
    return False

def is_gender_match(search_gender, data_gender):
    if (search_gender.lower() in data_gender.lower()):
        return True
    return False

def is_everything_match():
    pass

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = data_length // per_page + 1
    start_index = (page - 1) * per_page
    end_index = page * per_page
    return total_pages, start_index, end_index

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/users/")
def user():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default="", type=str)
    search_gender = request.args.get('gender', default="", type=str)

    data = get_data_from_file('src/user.csv')
    final_data, highlighted = filter_data(data, search_name, search_gender)
    total_pages, start_index, end_index =  get_pages_indexes(len(final_data), page)

    return render_template("users.html", users=final_data[start_index:end_index], total_pages=total_pages, page=page, 
                           search_name=search_name, search_gender=search_gender, highlighted=highlighted[start_index:end_index])

@app.route("/user_detail/<userid>")
def user_detail(userid):
    users = []
    with open('src/user.csv', newline='', encoding="utf-8") as user:
        reader = csv.DictReader(user, skipinitialspace=True)
        next(reader)
        for row in reader:
            if row['Id'] == userid :
                userinfo = row
                break
    return render_template("user_detail.html", userinfo=userinfo)

@app.route("/stores")
def store():
    stores = []
    with open('src/store.csv', newline='', encoding="utf-8") as store:
        reader = csv.DictReader(store, skipinitialspace=True)
        next(reader)
        for row in reader:
            stores.append(row)
    return render_template("stores.html", stores=stores)

@app.route("/store_detail/<storeid>")
def store_detail(storeid):
    with open('src/store.csv', newline='', encoding="utf-8") as store:
        reader = csv.DictReader(store, skipinitialspace=True)
        next(reader)
        for row in reader:
            if row['Id'] == storeid :
                storeinfo = row
                break
    return render_template("store_detail.html", storeinfo=storeinfo)

if __name__=="__main__":
    app.run(port=8080, debug=True)