from . import api
from flask import jsonify,request,session
from models import User,db

#  __init__ 폴더안에 있는 api 호출
@api.route('/users', methods=['GET','POST'])
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
            return jsonify({'error':'Input error'}), 400

        if password != re_password:
            return jsonify({'error':'password input error'}), 400

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

        # filter_by의 경우 =을 사용하고 filter의 경우 ==을 사용한다

        user = User.query.filter_by(id=id).first()
        if user.password != password:
            return jsonify({'error':'Password error'}), 400
        
        session['user'] = id
        return jsonify({'success':'ok'}), 200