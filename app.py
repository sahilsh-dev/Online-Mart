from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
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


if __name__ == '__main__':
    app.run()
