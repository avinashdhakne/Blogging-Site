from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open("config.json") as file:
    params = json.load(file)["params"]


app = Flask(__name__)

if(params["local_server"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_URI"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_URI"]

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


@app.route("/")
def home():
    return render_template("index.html", parameters=params)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if(request.method == "POST"):
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")
        entry = Contacts(name=name, phone_no=phone, msg=message,
                         email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        print(name, phone, email, message)
    return render_template("contact.html", parameters=params)


@app.route("/about")
def about():
    return render_template("about.html", parameters=params)


@app.route("/post")
def post():
    return render_template("post.html", parameters=params)


if __name__ == "__main__":
    app.run(debug=True)
