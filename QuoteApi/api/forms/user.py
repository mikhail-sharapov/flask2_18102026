from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class UserRegistrationForm(FlaskForm):
    username = StringField(label="username", validators=[DataRequired(), Length(min=4)])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=5, max=15)])
    repeat_password = PasswordField(label="repeat password", validators=[DataRequired(), Length(min=5, max=15), EqualTo("password", message="Password not confirmed")])


class UserLogInForm(FlaskForm):
    username = StringField(label="username", validators=[DataRequired(), Length(min=4)])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=5, max=15)])