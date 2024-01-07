from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, message='Username must be at least 3 characters long')])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    submit = SubmitField(label='Register')

    
class LoginForm(FlaskForm):
    username_or_email = StringField(label='Username or Email', validators=[DataRequired(), Length(min=3, message='Please enter correct username or email')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    submit = SubmitField(label='Login')
    remember_me = BooleanField(label='Remember Me')
