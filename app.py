from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

with open("config.json") as file:
    params = json.load(file)["params"]

app = Flask(__name__)

if(params["local_server"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_URI"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_URI"]

db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["gmail-user"],
    MAIL_PASSWORD=params["gmail-password"]
)

mail = Mail(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    img_name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)

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

        mail.send_message(
            "New mail from " + name,
            sender=email,
            recipients=[params["gmail-user"]],
            body=message + '\n' + phone
        )

    return render_template("contact.html", parameters=params)


@app.route("/about")
def about():
    return render_template("about.html", parameters=params)


@app.route("/post/<string:post_slug>")
def post_function(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", parameters=params, post=post)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
