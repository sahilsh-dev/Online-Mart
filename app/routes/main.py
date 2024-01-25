from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.forms import AddressForm, AccountDetailsForm
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.product import Product
from app.models.collection import Collection
from app.models.user import UserAddress
from datetime import datetime, timedelta

main = Blueprint('main', __name__)


@main.route('/')
def index():
    threshold_date = datetime.utcnow() - timedelta(days=100)  # Update this to 30 days
    new_arrivals = Product.query.filter(Product.created_at > threshold_date).all() 
    best_sellers_collection = Collection.query.get('best sellers').products
    best_sellers = [Product.query.get(collection_item.product_id) for collection_item in best_sellers_collection]
    return render_template(
        'index.html', 
        new_arrivals=new_arrivals, 
        best_sellers=best_sellers, 
        page='home'
    )


@main.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    orders = current_user.orders
    order_prices = [sum([item.price for item in order.order_items]) for order in orders]
    user_address = UserAddress.query.filter_by(user_id=current_user.id).first()
    
    address_form = AddressForm()
    account_form = AccountDetailsForm()
    if address_form.validate_on_submit():
        address_form.populate_obj(user_address)
        db.session.commit()
    if account_form.validate_on_submit():
        account_form.populate_obj(current_user)
        current_user.password_hash = generate_password_hash(
            account_form.password.data, 
            method='pbkdf2:sha256', 
            salt_length=8
        )
        if account_form.gender.data == 'Mr.':    current_user.gender = 'Male'
        elif account_form.gender.data == 'Mrs.': current_user.gender = 'Female'
        db.session.commit()
        
    return render_template(
        'account.html', 
        orders=orders, 
        order_prices=order_prices, 
        address=user_address,
        address_form=address_form,
        account_form=account_form
    )
    

@main.route('/cart')
def cart():
    return render_template('cart.html')
