from flask import Blueprint, request, render_template

from models.user import User
from view.common import get_pages_indexes, get_one_result, get_results, write_csv


user_bp = Blueprint('user', __name__)

# TODO: 프론트에서 처리
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
    
# TODO: 폴더 안에 user util user routes

@user_bp.route("/users/")
def users():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default="", type=str)
    search_gender = request.args.get('gender', default="", type=str)
    search_age = request.args.get('age', default=0, type=int)

    users = get_results("SELECT * FROM users")
        
    final_data, highlighted = filter_data(users, search_name, search_gender, search_age)
    total_pages, start_index, end_index =  get_pages_indexes(len(final_data), page)

    return render_template("users.html", users=final_data[start_index:end_index], highlighted=highlighted[start_index:end_index],
                           total_pages=total_pages, page=page, 
                           search_name=search_name, search_gender= search_gender, search_age = search_age)

@user_bp.route("/user_detail/")
def user_detail():
    user_id = request.args.get('id', default="", type=str)
        
    user_info = get_one_result("SELECT * FROM users WHERE id = ?", user_id)

    return render_template("common/detail.html", model="user", detail_info=user_info)

@user_bp.route("/user/register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        get = request.form
        user = User(get['Name'], get['Gender'], get['birthdate'], get['address']).generate()
        fieldnames = ['id', 'Name', 'Gender', 'age', 'birthdate', 'address']
        write_csv('src/user.csv', fieldnames, user)
        return render_template('register_complete.html', data=user)
    return render_template('user_register.html')