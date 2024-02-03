from flask import Blueprint, render_template, request
from app.models.product import Product
from app.models.cart import Cart, CartItem
from flask_login import current_user
from app.extensions import db
from app.models.wishlist import WishlistItem

product_group = Blueprint('product_group', __name__)

    
@product_group.route('/products/cart')
def my_cart():
    return render_template('cart.html')


@product_group.route('/products/cart/add/<int:product_id>', methods=['POST'])
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
        return ('<h2>Error! Please login again</h2>')


@product_group.route('/products/cart/remove/<int:cart_item_id>', methods=['POST'])
def remove_cart_item(cart_item_id):
    if current_user.is_authenticated and cart_item_id:
        delete_item = CartItem.query.get(cart_item_id) 
        db.session.delete(delete_item)
        db.session.commit()
        num_cart_items = len(current_user.cart.cart_items)
        cart_count_template = f'<span hx-swap-oob="true" id="num-cart-items" class="item-count">{num_cart_items}</span>'
        return render_template('components/cart-content.html', cart_items=current_user.cart.cart_items) + cart_count_template
    else:
        return ('<h2>Error! Please login again</h2>')
    
        
@product_group.route('/products/wishlist')
def my_wishlist():
    return render_template('wishlist.html')
        
        
@product_group.route('/products/wishlist/add/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    if current_user.is_authenticated and product_id:
        user_wishlist = current_user.wishlist
        new_wishlist_item = WishlistItem(wishlist_id=user_wishlist.id, product_id=product_id)
        db.session.add(new_wishlist_item)
        db.session.commit()
        
        wishlist_content_template = render_template('components/wishlist-content.html', wishlist_items=user_wishlist.wishlist_items)
        num_wishlist_items = len(current_user.wishlist.wishlist_items)
        wishlist_count_template = f'<span hx-swap-oob="true" id="num-wishlist-items" class="item-count">{num_wishlist_items}</span>'
        add_wishlist_template =  render_template('components/add-wishlist.html', wishlist_item=new_wishlist_item)
        return add_wishlist_template + wishlist_content_template + wishlist_count_template
    else:
        return ('<h2>Error! Please login again</h2>')


@product_group.route('/products/wishlist/remove/<int:wishlist_item_id>', methods=['POST'])
def remove_wishlist_item(wishlist_item_id):
    if current_user.is_authenticated and wishlist_item_id:
        delete_item = WishlistItem.query.get(wishlist_item_id) 
        product = delete_item.product
        db.session.delete(delete_item)
        db.session.commit()
        
        num_wishlist_items = len(current_user.wishlist.wishlist_items)
        wishlist_count_template = f'<span hx-swap-oob="true" id="num-wishlist-items" class="item-count">{num_wishlist_items}</span>'
        add_wishlist_template =  render_template('components/add-wishlist.html', product=product)
        wishlist_content_template = render_template('components/wishlist-content.html', wishlist_items=current_user.wishlist.wishlist_items)
        return add_wishlist_template + wishlist_content_template + wishlist_count_template
    else:
        return ('<h2>Error! Please login again</h2>')