import os
import stripe
from flask import Blueprint, render_template, redirect, request, url_for

checkout = Blueprint('checkout', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@checkout.route('/checkout/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print('User is checking out!')
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price_data': {
                        'unit_amount': int(9.99 * 100),
                        'product_data': {
                            'name': 'T-shirt',
                            'description': 'Comfortable cotton t-shirt',
                        },
                        'currency': 'inr',
                    },
                    'quantity': 1,
                },
            ],
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
    return render_template('checkout/success.html')


@checkout.route('/checkout/cancel')
def checkout_cancel():
    return render_template('checkout/cancel.html') 

