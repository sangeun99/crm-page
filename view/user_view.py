from flask import Blueprint, request, render_template

from models.user import User
from view.common import get_pages_indexes, get_one, get_all, insert_one


user_bp = Blueprint('user', __name__)

# TODO: 형광펜 프론트에서 처리

# TODO: 폴더 안에 user util user routes
@user_bp.route("/users/")
def users():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    search_gender = request.args.get('gender', default='', type=str)
    search_age = request.args.get('age', default=0, type=int)

    count_query = f"""SELECT COUNT(*) FROM users 
                     WHERE Name LIKE '%{search_name}%'"""
    
    if search_gender :
        count_query += f"AND Gender='{search_gender}'"

    if search_age :
        count_query += f"AND Age BETWEEN {search_age} AND CAST({search_age} AS int)+9"
        
    length = get_all(count_query)[0]['COUNT(*)']
    total_pages, per_page, start_index =  get_pages_indexes(length, page)

    query = f"SELECT * FROM users WHERE Name LIKE '%{search_name}%'"
    if search_gender :
        query += f"AND Gender='{search_gender}'"
    if search_age :
        query += f"AND Age BETWEEN {search_age} AND CAST({search_age+9} AS int)"
    query += f"LIMIT {start_index}, {per_page}"
    final_data = get_all(query)

    return render_template("users.html", users=final_data,
                           total_pages=total_pages, page=page, 
                           search_name=search_name, search_gender=search_gender, search_age=search_age)

@user_bp.route("/user_detail/")
def user_detail():
    user_id = request.args.get('id', default="", type=str)
        
    user_info = get_one("SELECT * FROM users WHERE id = ?", user_id)

    return render_template("common/detail.html", model="user", detail_info=user_info)

@user_bp.route("/user/register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        get = request.form
        user = User(get['name'], get['gender'], get['birthdate'], get['address']).generate()
        user_tuple = tuple(user.values())

        insert_one("insert into users values (?, ?, ?, ?, ?, ?)", user_tuple)

        return render_template('register_complete.html', data=user)
    return render_template('user_register.html')