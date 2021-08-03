from models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo

class RegisterForm(FlaskForm):
    id = StringField('id',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired(),EqualTo('re_password',message='비밀번호가 다릅니다.')])
    re_password = PasswordField('password',validators=[DataRequired()])

class LoginForm(FlaskForm):
    class Password_Check(object):
        def __init__(self,message=None):
            self.message = message

        def __call__(self,form,field):
            id = form['id'].data
            password = field.data
            user = User.query.filter_by(id=id).first()

            if user.password != password:
                raise ValueError("비밀번호가 다릅니다.")

    id = StringField('id',validators=[DataRequired()],description="아이디")
    password = PasswordField('password',validators=[DataRequired(),Password_Check()],description="비밀번호")