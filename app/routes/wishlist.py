from flask import Blueprint, render_template, request, make_response
from flask_login import current_user
from app.models.wishlist import WishlistItem
from app.extensions import db

wishlist = Blueprint('wishlist', __name__)


@wishlist.route('/products/wishlist')
def index():
    return render_template('wishlist.html')
        
        
@wishlist.route('/products/wishlist/content')
def update_wishlist_content():
    wishlist_content_template = render_template('components/wishlist-content.html', wishlist_items=current_user.wishlist.wishlist_items)
    num_wishlist_items = len(current_user.wishlist.wishlist_items)
    wishlist_count_template = f'<span hx-swap-oob="true" id="num-wishlist-items" class="item-count">{num_wishlist_items}</span>'
    return wishlist_content_template + wishlist_count_template
       
        
@wishlist.route('/products/wishlist/add/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    if current_user.is_authenticated and product_id:
        user_wishlist = current_user.wishlist
        new_wishlist_item = WishlistItem(wishlist_id=user_wishlist.id, product_id=product_id)
        db.session.add(new_wishlist_item)
        db.session.commit()
        
        product_page_content = render_template('components/add-wishlist.html', wishlist_item=new_wishlist_item)
        response = make_response(product_page_content)
        response.headers['HX-Trigger'] = 'updateWishlist'
        return response
    else:
        return ('<h2>Error! Please login</h2>')


@wishlist.route('/products/wishlist/remove/<int:wishlist_item_id>', methods=['POST'])
def remove_wishlist_item(wishlist_item_id):
    if current_user.is_authenticated and wishlist_item_id:
        delete_item = WishlistItem.query.get(wishlist_item_id) 
        product = delete_item.product
        db.session.delete(delete_item)
        db.session.commit()

        product_page_content = render_template('components/add-wishlist.html', product=product)
        response = make_response(product_page_content)
        response.headers['HX-Trigger'] = 'updateWishlist'
        return response
    else:
        return ('<h2>Error! Please login</h2>')