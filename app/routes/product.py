from flask import Blueprint, jsonify, render_template, url_for
from app.extensions import db
from flask_login import current_user
from app.models.product import Product
from app.models.wishlist import Wishlist, WishlistItem

product = Blueprint('product', __name__) 


@product.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    related_products = Product.query.filter(Product.id != product_id).all() 
    if current_user.is_authenticated:
        user_wishlist = current_user.wishlist
        if not user_wishlist:
            user_wishlist = Wishlist(user_id=current_user.id)
            db.session.add(user_wishlist)
            db.session.commit()
        cur_wishlist_item = WishlistItem.query.filter_by(wishlist_id=user_wishlist.id, product_id=product_id).first()
        
        return render_template (
            'product-details.html', 
            product=product, 
            related_products=related_products, 
            wishlist_item=cur_wishlist_item
        )
    return render_template(
        'product-details.html', 
        product=product, 
        related_products=related_products
    )


@product.route('/product/<int:product_id>')
def get_product_modal_data(product_id):
    product = Product.query.get(product_id)
    return jsonify({
        'title': product.product_name,
        'price': product.price,
        'description': product.description,
        'images': [url_for('static', filename='images/product/'+image.file_name) for image in product.images]
    })
