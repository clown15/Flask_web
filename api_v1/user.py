from . import api
from flask import jsonify,request
from models import User,db

#  __init__ 폴더안에 있는 api 호출
@api.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

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


    return jsonify()