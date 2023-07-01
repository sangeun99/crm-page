from flask import Flask, render_template, url_for, request
import csv

app = Flask(__name__, static_folder="static")

def get_data(filename, search_name="", search_gender=""):
    data = []
    highlighted = []
    with open(filename, newline='', encoding="utf-8") as user:
        reader = csv.DictReader(user, skipinitialspace=True)
        next(reader)
        for row in reader:
            if (is_name_match(search_name, row['Name']) and
                is_gender_match(search_gender, row['Gender'])) :
                data.append(row)
                match = [0 for _ in range(len(row['Name']))]
                if (search_name) :
                    for i in range(len(row['Name'])-len(search_name)+1):
                        if row['Name'][i:i+len(search_name)] == search_name:
                            match[i:i+len(search_name)] = [1 for _ in range(i, i+len(search_name))]
                highlighted.append(list(match))
    return data, highlighted

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
    end_index = page * per_page # T O D O
    return total_pages, start_index, end_index

@app.route("/users/")
def user():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default="", type=str)
    search_gender = request.args.get('gender', default="", type=str)

    keywords = ''
    keywords += "&name=" + search_name
    keywords += "&gender=" + search_gender

    data, highlighted = get_data('src/user.csv', search_name, search_gender)
    total_pages, start_index, end_index =  get_pages_indexes(len(data), page)

    return render_template("users.html", users=data[start_index:end_index], total_pages=total_pages, page=page, keywords=keywords, search_name=search_name, search_gender=search_gender, highlighted=highlighted[start_index:end_index])

@app.route("/user_detail/<userid>")
def user_detail(userid):
    users = []
    with open('src/user.csv', newline='', encoding="utf-8") as user:
        reader = csv.DictReader(user, skipinitialspace=True)
        next(reader)
        for row in reader:
            if row['Id'] == userid :
                userinfo = row
    return render_template("user_detail.html", userinfo=userinfo)

@app.route("/stores")
def store():
    stores = []
    with open('src/store.csv', newline='', encoding="utf-8") as store:
        reader = csv.DictReader(store)
        next(reader)
        for row in reader:
            clean_row = {key.strip(): value.strip() for key, value in row.items()}
            stores.append(clean_row)
    return render_template("stores.html", stores=stores)

@app.route("/store_detail/<storeid>")
def store_detail(storeid):
    with open('src/store.csv', newline='', encoding="utf-8") as store:
        reader = csv.DictReader(store)
        next(reader)
        for row in reader:
            clean_row = {key.strip(): value.strip() for key, value in row.items()}
            if clean_row['Id'] == storeid :
                storeinfo = clean_row
    return render_template("store_detail.html", storeinfo=storeinfo)

if __name__=="__main__":
    app.run(port=8080, debug=True)