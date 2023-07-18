from flask import Blueprint, request, render_template

from models.user import User
from view.common import get_pages_indexes, get_one, get_all, insert_one


user_bp = Blueprint('user', __name__)

def get_length_users(table_name, search_name, search_gender, search_age) :
    count_query = f"""SELECT COUNT(*) FROM {table_name} 
                     WHERE Name LIKE '%{search_name}%'"""
    
    if search_gender :
        count_query += " "
        count_query += f"AND Gender='{search_gender}'"

    if search_age :
        count_query += " "
        count_query += f"AND Age BETWEEN {search_age} AND CAST({search_age} AS int)+9"

    length = get_all(count_query)[0]['COUNT(*)']
    return length
        

# TODO: 형광펜 프론트에서 처리

# TODO: 폴더 안에 user util user routes
@user_bp.route("/users/")
def users():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    search_gender = request.args.get('gender', default='', type=str)
    search_age = request.args.get('age', default=0, type=int)

    length = get_length_users("users", search_name, search_gender, search_age)
    total_pages, per_page, start_index =  get_pages_indexes(length, page)

    query = f"SELECT * FROM users WHERE Name LIKE '%{search_name}%'"
    if search_gender :
        query += f" AND Gender='{search_gender}'"
    if search_age :
        query += f" AND Age BETWEEN {search_age} AND CAST({search_age+9} AS int)"
    query += f" LIMIT {start_index}, {per_page}"
    final_data = get_all(query)

    return render_template("users.html", users=final_data,
                           total_pages=total_pages, page=page, 
                           search_name=search_name, search_gender=search_gender, search_age=search_age)

@user_bp.route("/user_detail/")
def user_detail():
    user_id = request.args.get('id', default="", type=str)
        
    user_info = get_one("SELECT * FROM users WHERE id = ?", user_id)
    purchased_info_query = f"""select O.Id AS "order id", O.OrderAt AS "purchased date", S.Id AS "purchased location"
    from users U
    join orders O on O.userid = U.Id
    join stores S on S.Id = O.storeid
    where U.Id = "{user_id}";"""
    purchased_info = get_all(purchased_info_query)

    top_store_query = f'''select S.Name AS "store_name", count(O.Id) as "visited"
    from users U
    join orders O on O.userid = U.Id
    join stores S on S.Id = O.storeid
    where U.Id ="{user_id}"
    group by S.Id
    order by visited desc
    limit 5;'''
    top_store = get_all(top_store_query)

    top_item_query = f'''select I.Name, count(I.Id) as count_ordered
    from users U
    join orders O on O.userid = U.Id
    join stores S on S.Id = O.storeid
    join order_items OI on OI.orderid = O.Id
    join items I on OI.itemid = I.Id
    where U.Id ="{user_id}"
    group by I.Id
    order by count_ordered desc
    limit 5;'''
    top_item = get_all(top_item_query)
 
    return render_template("common/detail.html", model="user", detail_info=user_info,
                           purchased_info=purchased_info, top_store=top_store, top_item=top_item)

@user_bp.route("/user/register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        get = request.form
        user = User(get['name'], get['gender'], get['birthdate'], get['address']).generate()
        user_tuple = tuple(user.values())

        insert_one("insert into users values (?, ?, ?, ?, ?, ?)", user_tuple)

        return render_template('register_complete.html', data=user)
    return render_template('user_register.html')