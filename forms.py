from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, RadioField, DateField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, message='Username must be at least 3 characters long')])
    email = EmailField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4, message='Password must be at least 4 characters long')])
    submit = SubmitField(label='Register')

    
class LoginForm(FlaskForm):
    username_or_email = StringField(label='Username or Email', validators=[DataRequired(), Length(min=3, message='Please enter correct username or email')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4, message='Password must be at least 4 characters long')])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')


class AddressForm(FlaskForm):
    street = StringField(label='Street Address', validators=[DataRequired(), Length(min=3, message='Street name must be at least 6 characters long')])
    city = StringField(label='City', validators=[DataRequired(), Length(min=3, message='City name must be at least 3 characters long')])
    zip_code = StringField(label='Zip Code', validators=[DataRequired(), Length(min=6, message='Zip code must be at least 6 characters long')])
    country = StringField(label='Country', validators=[DataRequired(), Length(min=4, message='Country name must be at least 4 characters long')])
    submit = SubmitField(label='Update Address')


class AccountDetailsForm(FlaskForm):
    gender = RadioField(choices=[('Mr.'), ('Mrs.')], validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired(), Length(min=3, message='First name must be at least 3 characters long')])
    last_name = StringField(label='Last Name', validators=[DataRequired(), Length(min=3, message='Last name must be at least 3 characters long')])
    phone = StringField(label='Phone Number', validators=[DataRequired(), Length(min=10, message='Phone number must be at least 10 characters long')])
    password = PasswordField(label='New Password', validators=[DataRequired(), Length(min=4, message='Password must be at least 4 characters long')])
    birth_date = DateField(label='Birth Date', validators=[DataRequired()])
    receive_offers = BooleanField(label='Receive Offers From Our Partners')
    signup_newsletter = BooleanField(label='Sign Up For Our Newsletter')