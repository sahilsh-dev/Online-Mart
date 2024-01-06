import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import db, Product, Collection, Category
from datetime import datetime, timedelta
from hashlib import md5
from flask_login import UserMixin

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "any random string"
db.init_app(app)


def gravatar_url(email, size=50, rating='g', default='retro', force_default=False):
    hash_value = md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"


@app.context_processor
def inject_globals():
    categories = Category.query.all()
    return dict(categories=categories, gravatar_url=gravatar_url)


@app.route('/')
def home():
    threshold_date = datetime.utcnow() - timedelta(days=100)  # Update this to 30 days
    new_arrivals = Product.query.filter(Product.created_at > threshold_date).all() 
    best_sellers_collection = Collection.query.get('best sellers').products
    best_sellers = [Product.query.get(collection_item.product_id) for collection_item in best_sellers_collection]
    return render_template('index.html', 
                           new_arrivals=new_arrivals, 
                           best_sellers=best_sellers, 
                           page='home')


@app.route('/account')
def account():
    return render_template('account.html')


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
