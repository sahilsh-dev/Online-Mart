from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import Enum

db = SQLAlchemy()


class OrderStatusEnum(Enum):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'


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
    
    address = db.relationship('UserAddress', backref='user')
    cart = db.relationship('Cart', backref='user')   


class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.PROCESSING)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order_items = db.relationship('OrderItem', backref='order')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    cart_items = db.relationship('CartItem', backref='cart')
    

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product')


product_category = db.Table('product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    in_categories = db.relationship('Category', secondary=product_category, backref='products')
    images = db.relationship('ProductImage', backref='product') 
    
    def __repr__(self):
        return f'<Product {self.product_name}>'
    

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    file_name = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return f'<Student {self.file_name}>'


class Collection(db.Model):
    __tablename__ = 'collections'
    collection_name = db.Column(db.String(100), primary_key=True)
    products = db.relationship('CollectionItem', backref='collection')
     
    def __repr__(self):
        return f'<Collection {self.collection_name}>'
    

class CollectionItem(db.Model):
    __tablename__ = 'collection_items'
    id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(100), db.ForeignKey('collections.collection_name'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Category {self.category_name}>' 

