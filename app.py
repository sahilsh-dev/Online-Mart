import os
from flask import Flask, render_template, redirect, url_for, request
from models import db, Product

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

    
if __name__ == '__main__':
    app.run(debug=True)
