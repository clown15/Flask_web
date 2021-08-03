from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo

class RegisterForm(FlaskForm):
    id = StringField('userid',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired(),EqualTo('re_password')])
    re_password = PasswordField('password',validators=[DataRequired()])