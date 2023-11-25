from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


product_category = db.Table('product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)


class Product(db.Model):
    __tablename__ = "products" 
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    in_categories = db.relationship('Category', secondary=product_category, backref='products')
    images = db.relationship('ProductImage', backref='product', lazy=True) 
    
    def __repr__(self):
        return f'<Product {self.product_name}>'
    

class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    file_name = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return f'<Student {self.file_name}>'


class Collection(db.Model):
    __tablename__ = "collections"
    collection_name = db.Column(db.String(100), primary_key=True)
    products = db.relationship('CollectionItem', backref='collection', lazy=True)
     
    def __repr__(self):
        return f'<Collection {self.collection_name}>'
    

class CollectionItem(db.Model):
    __tablename__ = "collection_items"
    id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(100), db.ForeignKey('collections.collection_name'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), primary_key=True)
    
    def __repr__(self):
        return f'<Category {self.category_name}>' 
