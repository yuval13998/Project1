from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from models import *
from sqlalchemy import or_


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SECRET_KEY"] = "HakomonA"

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/register")
def register():
    return  render_template("register.html", msg="hidden")

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
             return  render_template("search.html",content="")
         else:
             return  render_template("message.html", msg=f"אמא שלך מוסרת שתהיה יצירתי")
    else:
         return  render_template("register.html", msg="visible")

@app.route("/signout",methods=["POST"])
def signout():
     session.clear()
     return  render_template("homepage.html")

@app.route("/login",methods=["POST"])
def login():
    userPass = request.form.get("password")
    userName = request.form.get("username")
    exist = User.query.filter_by(username = userName).first()
    if not exist:
        return  render_template("login.html", msg="user does not exist")
    else:
        if len(userPass) >= 6:
            if exist.password == userPass:
                session["user_id"] = exist.id
                return  render_template("search.html", content="")
            else:
                return  render_template("login.html", msg="wrong password")
        else:
            return  render_template("login.html", msg="password must contain at least 6 characterss!")

@app.route("/loginGet")
def loginGet():
    return  render_template("login.html")

@app.route("/search",methods=["GET","POST"])
def search():
      if request.method=="GET":
          if session.get("user_id") is None:
              return  render_template("homepage.html")
          else:
              return  render_template("search.html", content="")
      elif request.method=="POST":
          formcontent = request.form.get("content").lower()
          results= Book.query.filter(or_(Book.isbn.like(f"%{formcontent}%"),Book.title.like(f"%{formcontent}%"),Book.author.like(f"%{formcontent}%"),Book.year.like(f"%{formcontent}%"))).limit(10).all()
          return  render_template("search.html",results=results, content=f'Results for "{formcontent}":')
      else:
          return  render_template("homepage.html")

@app.route("/book/<string:isbn>")
def book(isbn):
    if Book.query.get(isbn) is not None:
        bookInfo = Book.query.get(isbn)
        reviews = bookInfo.reviews
        users = []
        for review in reviews:
             userName = User.query.get(review.user_id)
             users.append(userName.username)
        return  render_template("bookInfo.html",bookinfo=bookInfo, reviews=reviews, users=users)
    else:
        return  render_template("search.html")


@app.route("/addreview/<string:bookisbn>",methods=["GET","POST"])
def addreview(bookisbn):
    if request.method=="POST":
        book = Book.query.get(bookisbn)
        rate = int(request.form.get("ratereview"))
        content = request.form.get("reviewcontent")
        book.add_Rev(user_id=session["user_id"],rate=rate,content=content)
        reviews = book.reviews
        users = []
        for review in reviews:
            userName = User.query.get(review.user_id)
            users.append(userName.username)
        return  render_template("bookInfo.html",bookinfo=book,reviews=reviews,users=users)
    else:
        return  render_template("addreview.html",bookisbn=bookisbn)
