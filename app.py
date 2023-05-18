from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(100), unique=True, nullable=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)


db.create_all()


@app.route("/")
def home():
    other_items = Item.query.order_by(Item.added_date.desc()).limit(12).all()
    return render_template("index.html", other_items=other_items)


@app.route("/fashion")
def fashion():
    other_items = Item.query.filter(or_(Item.type == "t-shirt", Item.type == "shirt", Item.type == "skirt")).limit(12).all()
    return render_template("fashion.html", other_items=other_items)


@app.route("/electronic")
def electronic():
    other_items = Item.query.filter(or_(Item.type == "mobile", Item.type == "laptop", Item.type == "computer")).limit(12).all()
    return render_template("electronic.html", other_items=other_items)


@app.route("/jewellery")
def jewellery():
    other_items = Item.query.filter(or_(Item.type == "jhumka", Item.type == "necklace", Item.type == "kangan")).limit(12).all()
    return render_template("jewellery.html", other_items=other_items)


@app.route("/items/<string:item_type>")
def load_items(item_type):
    items = Item.query.filter_by(type=item_type).all()
    return render_template("items.html", items=items)


@app.route("/buy/<int:item_id>")
def buy_item(item_id):
    item_to_buy = Item.query.get(item_id)
    return render_template("buy.html", item_data=item_to_buy)


if __name__ == "__main__":
    app.run(debug=True)
