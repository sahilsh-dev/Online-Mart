from flask import render_template
from flask_login import current_user
from hashlib import md5
from app.extensions import login_manager
from app.models.category import Category
from app.models.user import User


def gravatar_url(email='email@gmail.com', size=50, rating='g', default='mp', force_default=False):
    if current_user.is_authenticated:
        email = current_user.email
        default = 'retro'
    hash_value = md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"


def inject_globals():
    categories = Category.query.all()
    profile_img_url = gravatar_url()
    cart_items = current_user.cart.cart_items if current_user.is_authenticated else []
    total_cart_price = sum([item.product.price * item.quantity for item in cart_items])
    wishlist_items = current_user.wishlist.wishlist_items if current_user.is_authenticated else []
    return dict(
        categories=categories, 
        profile_img_url=profile_img_url, 
        cart_items=cart_items,
        wishlist_items=wishlist_items,
        total_cart_price=total_cart_price,
        num_wishlist_items=len(wishlist_items),
        num_cart_items=len(cart_items)
    )


def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
