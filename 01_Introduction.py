from flask import Flask

app = Flask(__name__)
print(__name__)


@app.route("/")
def home():
    return "Hello Flask"


@app.route("/home")
def home1():
    return "This is home"


app.run(debug=True)
