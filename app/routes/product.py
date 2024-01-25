from flask import Blueprint, jsonify, render_template, url_for, request
from app.models.product import Product

product = Blueprint('product', __name__) 


@product.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    related_products = Product.query.filter(Product.id != product_id).all() 
    return render_template('product-details.html', product=product, related_products=related_products)


@product.route('/product/<int:product_id>')
def get_product_modal_data(product_id):
    product = Product.query.get(product_id)
    return jsonify({
        'title': product.product_name,
        'price': product.price,
        'description': product.description,
        'images': [url_for('static', filename='images/product/'+image.file_name) for image in product.images]
    })


@product.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')