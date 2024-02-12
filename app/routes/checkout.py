import os
import stripe
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user
from app.extensions import db

checkout = Blueprint('checkout', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@checkout.route('/checkout/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print('User is checking out!')
    checkout_data = []
    for item in current_user.cart.cart_items:
        item_data = {
            'price_data': {
                'unit_amount': item.product.price * 100,
                'product_data': {
                    'name': item.product.product_name,
                },
                'currency': 'inr',
            },
            'quantity': item.quantity
        }
        checkout_data.append(item_data)
    print(checkout_data)    
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = checkout_data,
            mode='payment',
            success_url = url_for('checkout.checkout_success', _external=True),
            cancel_url = url_for('checkout.checkout_cancel', _external=True)
        )
    except Exception as e:
        print(str(e))
        return str(e)
    return redirect(checkout_session.url, code=303)


@checkout.route('/checkout/success')
def checkout_success():
    db.session.delete(current_user.cart.cart_items)
    db.session.commit()
    return render_template('checkout/success.html')


@checkout.route('/checkout/cancel')
def checkout_cancel():
    return render_template('checkout/cancel.html') 

