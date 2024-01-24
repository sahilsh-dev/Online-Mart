from app.extensions import db
from flask_login import UserMixin
from .order import Order
from .cart import Cart


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    phone = db.Column(db.Integer)
     
    address = db.relationship('UserAddress', backref='user')
    cart = db.relationship('Cart', backref='user', uselist=False)   
    orders = db.relationship('Order', backref='user')

    def __repr__(self) -> str:
        return f'<User {self.username}>'
  

class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False)
