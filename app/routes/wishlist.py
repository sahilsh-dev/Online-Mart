from flask import Blueprint, render_template, make_response
from flask_login import current_user, login_required
from app.models.wishlist import WishlistItem
from app.extensions import db
from .auth import htmx_login_required

wishlist = Blueprint('wishlist', __name__)


@wishlist.route('/wishlist')
@login_required
def index():
    return render_template('wishlist.html')
        
        
@wishlist.route('/wishlist/content')
@htmx_login_required
def update_wishlist_content():
    wishlist_content_template = render_template('components/wishlist-content.html', wishlist_items=current_user.wishlist.wishlist_items)
    num_wishlist_items = len(current_user.wishlist.wishlist_items)
    wishlist_count_template = f'<span hx-swap-oob="true" id="num-wishlist-items" class="item-count">{num_wishlist_items}</span>'
    return wishlist_content_template + wishlist_count_template
       
        
@wishlist.route('/wishlist/add/<int:product_id>', methods=['POST'])
@htmx_login_required
def add_to_wishlist(product_id):
    user_wishlist = current_user.wishlist
    add_wishlist_item = WishlistItem.query.filter_by(wishlist_id=user_wishlist.id, product_id=product_id).first()
    if not add_wishlist_item:
        add_wishlist_item = WishlistItem(wishlist_id=user_wishlist.id, product_id=product_id)
        db.session.add(add_wishlist_item)
        db.session.commit()

    product_page_content = render_template('components/add-wishlist.html', wishlist_item=add_wishlist_item)
    item_box_content = f'<i hx-swap-oob="true" id="action-link-item-{product_id}" class="fa-heart fa-solid"></i>'
    response = make_response(product_page_content + item_box_content)
    response.headers['HX-Trigger'] = 'updateWishlist'
    return response


@wishlist.route('/wishlist/remove/<int:wishlist_item_id>', methods=['POST'])
@htmx_login_required
def remove_wishlist_item(wishlist_item_id):
    delete_item = WishlistItem.query.get(wishlist_item_id) 
    product = delete_item.product
    db.session.delete(delete_item)
    db.session.commit()

    product_page_content = render_template('components/add-wishlist.html', product=product)
    response = make_response(product_page_content)
    response.headers['HX-Trigger'] = 'updateWishlist'
    return response


@wishlist.route('/wishlist/table/<int:wishlist_item_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist_table(wishlist_item_id):
    delete_item = WishlistItem.query.get(wishlist_item_id)
    db.session.delete(delete_item)
    db.session.commit()
    return render_template('components/wishlist-table-content.html', wishlist_items=current_user.wishlist.wishlist_items)    

