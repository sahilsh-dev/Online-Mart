from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.cart import Cart
from app.models.wishlist import Wishlist

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if not (email.endswith('.com') or email.endswith('.in')):
            flash('Please enter a valid email address')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(username=form.username.data).first():
            flash("This username already exists, kindly choose a new username")
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first(): 
            flash("You've already signed up with that email, Log in instead")
            return redirect(url_for('auth.login')) 

        secure_password = generate_password_hash(
            form.password.data, 
            method='pbkdf2:sha256', 
            salt_length=8
        )
        new_user = User(
            username=form.username.data,
            password_hash=secure_password,
            email=email,
        )
        new_user.cart = Cart()
        new_user.wishlist = Wishlist()
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        if username_or_email.endswith('.com') or username_or_email.endswith('.in'):
            saved_user = User.query.filter_by(email=username_or_email).first()
        else:
            saved_user = User.query.filter_by(username=username_or_email).first()
        
        entered_password = form.password.data
        remember_me = form.remember_me.data
        if not saved_user:
            flash("That email does not exist! Please try again")
        elif check_password_hash(saved_user.password_hash, entered_password):
            login_user(saved_user, remember=remember_me)
            return redirect(url_for('main.index'))
        else:
            flash("The password is incorrect! Please try again") 
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
