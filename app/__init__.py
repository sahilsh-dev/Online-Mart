from flask import Flask
import os
from app.extensions import db, login_manager 


def create_app(): 
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'any random string'

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.globals import inject_globals
    app.context_processor(inject_globals)

    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.auth import auth
    app.register_blueprint(auth)
       
    from app.routes.shop import shop
    app.register_blueprint(shop)
    
    from app.routes.product import product
    app.register_blueprint(product)
    
    from app.routes.cart import cart
    app.register_blueprint(cart)
    
    from app.routes.wishlist import wishlist
    app.register_blueprint(wishlist)
    
    from app.routes.checkout import checkout
    app.register_blueprint(checkout)
    
    return app
    