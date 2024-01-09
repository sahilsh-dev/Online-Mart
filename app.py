import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from models import db, Product, Collection, Category, User, UserAddress
from datetime import datetime, timedelta
from hashlib import md5
from forms import RegisterForm, LoginForm, AddressForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any random string'
login_manager = LoginManager(app)
db.init_app(app)


def gravatar_url(email='email@gmail.com', size=50, rating='g', default='mp', force_default=False):
    if current_user.is_authenticated:
        email = current_user.email
        default = 'retro'
    hash_value = md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"


@app.context_processor
def inject_globals():
    categories = Category.query.all()
    profile_img_url = gravatar_url()
    return dict(categories=categories, profile_img_url=profile_img_url)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if not (email.endswith('.com') or email.endswith('.in')):
            flash('Please enter a valid email address')
            return redirect(url_for('register'))
        if User.query.filter_by(username=form.username.data).first():
            flash("This username already exists, kindly choose a new username")
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first(): 
            flash("You've already signed up with that email, Log in instead")
            return redirect(url_for('login')) 

        secure_password = generate_password_hash(
            form.password.data, 
            method='pbkdf2:sha256', 
            salt_length=8
        )
        new_user = User(
            username=form.username.data,
            password_hash = secure_password,
            email = email,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('home'))
        else:
            flash("The password is incorrect! Please try again") 
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    orders = current_user.orders
    order_prices = [sum([item.price for item in order.order_items]) for order in orders]
    user_address = UserAddress.query.filter_by(user_id=current_user.id).first()
    form = AddressForm()

    if form.validate_on_submit():
        form.populate_obj(user_address)
        db.session.commit()
    return render_template(
        'account.html', 
        orders=orders, 
        order_prices=order_prices, 
        address=user_address,
        form=form
    )


@app.route('/product/<int:product_id>')
def product_modal_data(product_id):
    product = Product.query.get(product_id)
    return jsonify({
        'title': product.product_name,
        'price': product.price,
        'description': product.description,
        'images': [url_for('static', filename='images/product/'+image.file_name) for image in product.images]
    })


@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route('/shop/search')
def shop_search():
    search_term = request.args.get('search_term')
    if not search_term:
        return jsonify([])
    products = Product.query.filter(
        (Product.product_name.ilike(f'%{search_term}%')) |
        (Product.description.ilike(f'%{search_term}%'))
    ).limit(5).all()
    
    return jsonify([{
        'title': product.product_name, 
        'url': url_for('product_details', product_id=product.id)} for product in products
    ])


@app.route('/shop/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    related_products = Product.query.filter(Product.id != product_id).all() 
    return render_template('product-details.html', product=product, related_products=related_products)


@app.route('/shop/collection/<collection_name>')
def shop_collection(collection_name):
    collection = Collection.query.get(collection_name).products
    products = [Product.query.get(collection_item.product_id) for collection_item in collection]
    return render_template('shop.html', products=products)


@app.route('/shop/categories')
def shop_category():
    categories = request.args.getlist('category_names')
    products = Product.query.join(Product.in_categories).filter(Category.category_name.in_(categories)).all()
    return render_template('shop.html', products=products)
 

if __name__ == '__main__':
    app.run(debug=True)
