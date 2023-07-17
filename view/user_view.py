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

    if not search_gender :
        search_gender_tup = ('Female', 'Male')
    else :
        search_gender_tup = tuple(search_gender)

    # users = get_all("SELECT * FROM users")
    length = get_all(f"""SELECT COUNT(*)
                     FROM users 
                     WHERE Name LIKE '%{search_name}%' 
                     AND Gender IN {search_gender_tup}""")[0]['COUNT(*)']
    total_pages, start_index, end_index =  get_pages_indexes(length, page)
    final_data = get_all(f"""SELECT * FROM users
                         WHERE Name LIKE '%{search_name}%'
                         AND Gender IN {search_gender_tup}
                         LIMIT {start_index}, {end_index}""")

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