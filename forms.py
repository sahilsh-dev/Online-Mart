from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, message='Username must be at least 3 characters long')])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4, message='Password must be at least 8 characters long')])
    submit = SubmitField(label='Register')

    
class LoginForm(FlaskForm):
    username_or_email = StringField(label='Username or Email', validators=[DataRequired(), Length(min=3, message='Please enter correct username or email')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4, message='Password must be at least 8 characters long')])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')


class AddressForm(FlaskForm):
    street = StringField(label='Street Address', validators=[DataRequired(), Length(min=3, message='Street name must be at least 6 characters long')])
    city = StringField(label='City', validators=[DataRequired(), Length(min=3, message='City name must be at least 3 characters long')])
    zip_code = StringField(label='Zip Code', validators=[DataRequired(), Length(min=6, message='Zip code must be at least 6 characters long')])
    country = StringField(label='Country', validators=[DataRequired(), Length(min=4, message='Country name must be at least 4 characters long')])
    submit = SubmitField(label='Update Address')