import os
from flask import Flask,render_template
from flask import request,redirect,session
from models import db,User
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm,LoginForm
from sqlalchemy.exc import IntegrityError
from api_v1 import api as api_v1
from flask_jwt import JWT

app = Flask(__name__)
app.register_blueprint(api_v1,url_prefix='/api/v1')
# view부분
@app.route("/register/",methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # id = request.form.get('id')
        # name = request.form.get('name')
        # password = request.form.get('password')
        # re_password = request.form.get('re-password')

        user = User()
        user.id = form.data.get('id')
        user.password = form.data.get('password')
        user.name = form.data.get('name')

        try:
            db.session.add(user)
            db.session.commit()

            return redirect('/')
        except IntegrityError:
            db.session.rollback()

    return render_template("register.html",form=form)

@app.route("/login/",methods=['GET','POST'])
def login():
    # 이미 로그인 했을경우
    if 'user' in session:
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        # 기본키로 객체 호출
        # user = User.query.get(form.data.get('id'))
        # 로그인에 대한 검증은 forms.py에있는 Password_Check에서 진행
        # validate_on_submit이 실행될때 form 데이터에 대해 검증
        session['user'] = form.data.get('id')

        return redirect('/')

    return render_template('login.html',form=form)

@app.route("/logout/")
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route("/")
def hello_world():
    if 'user' in session:
        return render_template("hello.html",user=session['user'])    
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
    # -------- csrf 설정 ------------------
    app.config['SECRET_KEY'] = 'sdnajkfnwejknvjkfda'

    # csrf token 설정
    # csrf = CSRFProtect()
    # csrf.init_app(app)
    # -------------------------------------
    # db설정값 초기화
    db.init_app(app)
    db.app = app
    # db 생성
    db.create_all()

    def authenticate(username,password):
        user = User.query.filter(user.id==username).first()
        if user.password == password:
            return user

    jwt = JWT(app,authenticate)

    app.run(host='0.0.0.0',port='5000',debug=True)