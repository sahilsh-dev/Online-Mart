import os
from flask import Flask, render_template, redirect, url_for, request
from models import db, Product, Collection
from datetime import datetime, timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    threshold_date = datetime.utcnow() - timedelta(days=30)
    new_arrivals = Product.query.filter(Product.created_at > threshold_date).all()
    best_sellers_collection = Collection.query.get('best sellers').products
    best_sellers = [Product.query.get(collection_item.product_id) for collection_item in best_sellers_collection]
    return render_template('index.html', new_arrivals=new_arrivals, best_sellers=best_sellers, page='home')


@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route('/shop/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    return render_template('product-details.html', product=product)
     
    
if __name__ == '__main__':
    app.run(debug=True)
