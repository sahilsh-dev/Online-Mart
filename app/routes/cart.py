from flask import Blueprint, render_template, request
from app.models.product import Product
from app.models.cart import CartItem
from flask_login import current_user, login_required
from app.extensions import db
from .auth import htmx_login_required

cart = Blueprint('cart', __name__)
    

@cart.route('/cart')
@login_required
def index():
    total_cart_cost = sum([item.product.price * item.quantity for item in current_user.cart.cart_items])
    return render_template('cart.html', total_cart_cost=total_cart_cost)
    
    
def handle_add_to_cart(user_cart, product_id, quantity=1):
    cart_item = CartItem.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()    
    product = Product.query.get(product_id)
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
    else:
        new_cart_item = CartItem(cart_id=user_cart.id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)
        db.session.commit()
    return product


@cart.route('/cart/add/<int:product_id>', methods=['POST'])
@htmx_login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity')) if request.form.get('quantity') else 1
    user_cart = current_user.cart
    new_cart_product = handle_add_to_cart(user_cart, product_id, quantity)
            
    add_item_modal_template = render_template('components/add-cart-modal.html', product=new_cart_product, item_quantity=quantity) 
    cart_content_template = render_template('components/cart-content.html', cart_items=user_cart.cart_items)
    
    num_cart_items = len(current_user.cart.cart_items)
    cart_count_template = f'<span hx-swap-oob="true" id="num-cart-items" class="item-count">{num_cart_items}</span>'
    return add_item_modal_template + cart_content_template + cart_count_template


@cart.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
@htmx_login_required
def remove_cart_item(cart_item_id):
    delete_item = CartItem.query.get(cart_item_id) 
    db.session.delete(delete_item)
    db.session.commit()
    num_cart_items = len(current_user.cart.cart_items)
    cart_count_template = f'<span hx-swap-oob="true" id="num-cart-items" class="item-count">{num_cart_items}</span>'
    return render_template('components/cart-content.html', cart_items=current_user.cart.cart_items) + cart_count_template


@cart.route('/cart/table/<int:cart_item_id>', methods=['DELETE'])
@login_required
def remove_from_cart_table(cart_item_id):
    delete_item = CartItem.query.get(cart_item_id)
    db.session.delete(delete_item)
    db.session.commit()
    return render_template('components/cart-table-content.html', cart_items=current_user.cart.cart_items)


@cart.route('/cart/table', methods=['POST'])
@htmx_login_required
def update_cart_table(): 
    total_cart_cost = 0
    for item in current_user.cart.cart_items:
        item.quantity = int(request.form.get(f'quantity_{item.id}'))
        total_cart_cost += item.product.price * item.quantity
    db.session.commit()

    cart_table_template = render_template ('components/cart-table-content.html', cart_items=current_user.cart.cart_items)
    cart_totals_template = render_template('components/cart-totals.html', total_cart_cost=total_cart_cost)
    return cart_table_template + cart_totals_template
