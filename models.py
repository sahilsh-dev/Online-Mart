from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products" 
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    images = db.relationship('ProductImage', backref='product', lazy=True) 
    
    def __repr__(self):
        return f'<Product {self.id} - {self.product_name}>'
    

class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    file_name = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return f'<Student {self.file_name}>'
