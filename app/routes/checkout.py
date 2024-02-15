import os
import stripe
from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required
from app.extensions import db
from app.models.order import Order, OrderItem, OrderStatusEnum

checkout = Blueprint('checkout', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@checkout.route('/checkout/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
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
    new_order = Order(user_id=current_user.id, status=OrderStatusEnum.PROCESSING)
    for item in current_user.cart.cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        new_order.order_items.append(order_item)
        db.session.delete(item)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('main.index', checkout_success=True))


@checkout.route('/checkout/cancel')
def checkout_cancel():
    return redirect(url_for('main.index', checkout_success=False))

