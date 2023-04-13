from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    return render_template("index.html")


@app.route("/fashion")
def fashion():
    return render_template("fashion.html")


@app.route("/electronic")
def electronic():
    return render_template("electronic.html")


@app.route("/jewellery")
def jewellery():
    return render_template("jewellery.html")


@app.route("/items/<string:item_type>")
def load_items(item_type):
    items = Item.query.filter_by(type=item_type).all()
    return render_template("items.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
