from flask import Blueprint, render_template, request
from app.models.product import Product
from app.models.cart import Cart, CartItem
from flask_login import current_user
from app.extensions import db
from app.models.wishlist import WishlistItem

cart = Blueprint('cart', __name__)

    
@cart.route('/products/cart')
def index():
    return render_template('cart.html')


@cart.route('/products/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity'))
    if current_user.is_authenticated and quantity and product_id:
        user_cart = current_user.cart
        cart_item = CartItem.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()    
        product = Product.query.get(product_id)
        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()
        else:
            new_cart_item = CartItem(cart_id=user_cart.id, product_id=product_id, quantity=quantity)
            db.session.add(new_cart_item)
            db.session.commit()
            
        add_item_modal_template = render_template('components/add-cart-modal.html', product=product, item_quantity=quantity) 
        cart_content_template = render_template('components/cart-content.html', cart_items=user_cart.cart_items)
        
        num_cart_items = len(current_user.cart.cart_items)
        cart_count_template = f'<span hx-swap-oob="true" id="num-cart-items" class="item-count">{num_cart_items}</span>'
        return add_item_modal_template + cart_content_template + cart_count_template
    else:
        return ('<h2>Error! Please login</h2>')


@cart.route('/products/cart/remove/<int:cart_item_id>', methods=['POST'])
def remove_cart_item(cart_item_id):
    if current_user.is_authenticated and cart_item_id:
        delete_item = CartItem.query.get(cart_item_id) 
        db.session.delete(delete_item)
        db.session.commit()
        num_cart_items = len(current_user.cart.cart_items)
        cart_count_template = f'<span hx-swap-oob="true" id="num-cart-items" class="item-count">{num_cart_items}</span>'
        return render_template('components/cart-content.html', cart_items=current_user.cart.cart_items) + cart_count_template
    else:
        return ('<h2>Error! Please login</h2>')
