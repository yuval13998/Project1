from flask import Flask, render_template, jsonify, request
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def firstPage():
    return render_template("register.html")


@app.route("/newUser",methods=["POST"])
def newUser():
    userName = request.form.get("username")
    userPass = request.form.get("password")
    exist = User.query.filter_by(username = userName).all()
    if not exist:
        newuser = User(username = userName, password = userPass)
        db.session.add(newuser)
        db.session.commit()
        return  render_template("error.html", msg=f"wellcommmmmmmmmmmm  {userName}, {userPass}")
    else:
        return  render_template("error.html", msg=f"אמא שלך")
