from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/codingthunder'
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
    return render_template("index.html")


@app.route("/contact", methods=["GET","POST"])
def contact():
    if(request.method == "POST"):
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")
        entry = Contacts(name = name, phone_no = phone, msg = message, email = email, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        print(name, phone, email, message)
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post")
def post():
    return render_template("post.html")


if __name__ == "__main__":
    app.run(debug=True)
