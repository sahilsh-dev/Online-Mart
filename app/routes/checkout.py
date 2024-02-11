import os
import stripe
from flask import Blueprint, render_template, redirect, request, url_for

checkout = Blueprint('checkout', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@checkout.route('/checkout/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print('User is checking out!')
    

@checkout.route('/checkout/success')
def checkout_success():
    return render_template('checkout/success.html')


@checkout.route('/checkout/cancel')
def checkout_cancel():
    return render_template('checkout/cancel.html') 

