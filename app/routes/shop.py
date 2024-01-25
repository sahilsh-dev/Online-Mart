from flask import Blueprint, render_template, request, jsonify, url_for
from app.models.product import Product
from app.models.collection import Collection
from app.models.category import Category

shop = Blueprint('shop', __name__)


@shop.route('/shop')
def index():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@shop.route('/shop/search')
def item_search():
    search_term = request.args.get('search_term')
    if not search_term:
        return jsonify([])
    products = Product.query.filter(
        (Product.product_name.ilike(f'%{search_term}%')) |
        (Product.description.ilike(f'%{search_term}%'))
    ).limit(5).all()
    
    return jsonify([{
        'title': product.product_name, 
        'url': url_for('product.product_details', product_id=product.id)} for product in products
    ])


@shop.route('/shop/collection/<collection_name>')
def shop_collection(collection_name):
    collection = Collection.query.get(collection_name).products
    products = [Product.query.get(collection_item.product_id) for collection_item in collection]
    return render_template('shop.html', products=products)


@shop.route('/shop/categories')
def shop_category():
    categories = request.args.getlist('category_names')
    products = Product.query.join(Product.in_categories).filter(Category.category_name.in_(categories)).all()
    return render_template('shop.html', products=products)
