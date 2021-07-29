import os
from flask import Flask,render_template
from flask import request,redirect
from models import db,User

app = Flask(__name__)

# view부분
@app.route("/register/",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        if id and name and password and re_password and (password == re_password):
            user = User()
            user.id = id
            user.password = password
            user.name = name

            db.session.add(user)
            db.session.commit()

            return redirect('/')

    return render_template("register.html")


@app.route("/")
def hello_world():
    return render_template("hello.html")

# 직접 실행한 경우
if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir,'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+dbfile
    # True로 설정하면 각 리퀘스트의 끝에 데이터베이스 변경사항을 자동 커밋(저장,반영)한다.
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
    # DB변경 사항을 추적할지에 대한 변수로 추적을 위해서는 추가 메모리가 필요하며 추적이 필요없다면 false로 설정해야한다.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    # db설정값 초기화
    db.init_app(app)
    db.app = app
    # db 생성
    db.create_all()

    app.run(host='0.0.0.0',port='5000',debug=True)