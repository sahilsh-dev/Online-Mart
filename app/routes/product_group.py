from flask import Blueprint, render_template, request
from app.models.product import Product
from app.models.cart import Cart, CartItem
from flask_login import current_user
from app.extensions import db

product_group = Blueprint('product_group', __name__)

    
@product_group.route('/products/cart')
def my_cart():
    return render_template('cart.html')


@product_group.route('/products/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity'))
    if current_user.is_authenticated:
        user_cart = current_user.cart
        cart_item = CartItem.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()    
        product = Product.query.get(product_id)
        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()
        else:
            cart_item = CartItem(cart_id=user_cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()
        add_item_template = render_template('components/add-cart-modal.html', product=product, item_quantity=quantity) 
        cart_content_template = render_template('components/cart-content.html', cart_items=user_cart.cart_items)
        return add_item_template + cart_content_template
    else:
        return ('<h2>You need to login to add items to cart</h2>')


@product_group.route('/products/cart/remove', methods=['POST'])
def delete_cart_item():
    cart_item_id = request.form.get('cart_item_id')
    if current_user.is_authenticated and cart_item_id:
        cart_item_id = int(cart_item_id)
        delete_item = CartItem.query.get(cart_item_id) 
        db.session.delete(delete_item)
        db.session.commit()
        return render_template('components/cart-content.html', cart_items=current_user.cart.cart_items)