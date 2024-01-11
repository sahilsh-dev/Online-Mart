from app.extensions import db


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
    

