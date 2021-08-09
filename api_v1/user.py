from . import api
from flask import jsonify,request,session
from models import User,db
from flask_jwt import jwt_required

#  __init__ 폴더안에 있는 api 호출
@api.route('/users', methods=['GET','POST'])
@jwt_required()
def users():
    if request.method == 'POST':
        # form사용시
        # id = request.form.get('id')
        # name = request.form.get('name')
        # password = request.form.get('password')
        # re_password = request.form.get('re_password')
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        password = data.get('password')
        re_password = data.get('re_password')

        if not (id and name and password and re_password):
            return jsonify({'error':'모든값을 입력해야 합니다.'}), 400

        if password != re_password:
            return jsonify({'error':'입력한 비밀번호가 서로 다릅니다.'}), 400

        user = User()
        user.id = id
        user.name = name
        user.password = password

        db.session.add(user)
        db.session.commit()

        return jsonify(), 201

    users = User.query.all()
    return jsonify([user.serialize for user in users])

@api.route('/users/<uid>',methods=['GET','PUT','DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = User.query.filter(User.id == uid).first()

        return jsonify(user.serialize)
    
    elif request.methods == 'DELETE':
        User.query.delete(User.id == uid)

        return jsonify(),204
    else:
        data = request.get_json()
        """
        id = data.get('id')
        name = data.get('name')
        password = data.get('password')

        updated_data = {}
        if name:
            updated_data['name']=name
        if password:
            updated_data['password']=password
        
        User.query.filter(User.id == uid).update(updated_data)
        """
        User.query.filter(User.id == uid).update(data)
        user = User.query.filter(User.id == uid).first()

        return jsonify(user.serialize)

@api.route('/user/login',methods=['POST'])
def login():
    data = request.get_json()
    id = data.get('id')
    password = data.get('password')

    if not (id and password):
        return jsonify({'error':'Input error'}), 400

    # filter_by의 경우 =로 비교하고 colum_name=value의 형식을 사용한다.
    #  filter의 경우 ==을 통해 비교하고 db.colum_name==value의 형식 사용
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error':'아이디를 잘못 입력했습니다.'}), 400
    if user.password != password:
        return jsonify({'error':'비밀번호를 잘못 입력했습니다.'}), 400
    
    session['user'] = id
    return jsonify({'success':'ok'}), 200