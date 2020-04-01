from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from models import *
import time


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SECRET_KEY"] = "HakomonA"

@app.route("/")
def homepage():
    return render_template("register.html",msg="hidden")

@app.route("/newUser",methods=["POST"])
def newUser():
    userPass = request.form.get("password")
    if len(userPass) >= 6:
         userName = request.form.get("username")
         exist = User.query.filter_by(username = userName).all()
         if not exist:
             newuser = User(username = userName, password = userPass)
             db.session.add(newuser)
             db.session.commit()
             newuser = User.query.filter_by(username = userName).first()
             session["user_id"] = newuser.id
             return  render_template("error.html", msg=f"the new id is {session['user_id']}")
         else:
             return  render_template("error.html", msg=f"אמא שלך מוסרת שתהיה יצירתי")
    else:
         return  render_template("register.html", msg="visible")

@app.route("/signout",methods=["POST"])
def signout():
     session.clear()
     return  render_template("homepage.html")
