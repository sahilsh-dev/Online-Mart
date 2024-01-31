from flask import Blueprint, render_template, request
from app.models.product import Product
from app.models.cart import Cart, CartItem
from flask_login import current_user
from app.extensions import db

product_group = Blueprint('product_group', __name__)

    
@product_group.route('/products/cart')
def cart():
    return render_template('cart.html')


@product_group.route('/products/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity'))
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()    
        product = Product.query.get(product_id)
        if cart_item and cart_item.quantity != quantity:
            cart_item.quantity = quantity
            db.session.commit()
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()
        return render_template('components/add-cart-modal.html', product=product, item_quantity=quantity)
    else:
        return ('<h2>You need to login to add items to cart</h2>')
            