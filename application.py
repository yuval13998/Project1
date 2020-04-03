from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from models import *
from booksinfo import *
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

@app.route("/login",methods=["POST", "GET"])
def login():
    if request.method=="GET":
        return  render_template("login.html")
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


@app.route("/search",methods=["GET","POST"])
def search():
      if session.get("user_id") is None:
           return  render_template("homepage.html")
      elif request.method=="GET":
        return  render_template("search.html", content="")
      else:
          formcontent = request.form.get("content").lower()
          results= Book.query.filter(or_(Book.isbn.like(f"%{formcontent}%"),Book.title.like(f"%{formcontent}%"),Book.author.like(f"%{formcontent}%"),Book.year.like(f"%{formcontent}%"))).limit(10).all()
          return  render_template("search.html",results=results, content=f'Results for "{formcontent}":')

@app.route("/book/<string:isbn>")
def book(isbn):
    if session.get("user_id") is None:
          return  render_template("homepage.html")
    if Book.query.get(isbn) is not None:
        bookInfo = Book.query.get(isbn)
        reviews = bookInfo.reviews
        avRate = bookInfo.getGoodreads()
        users = bookInfo.listofnames(reviews)
        bookextra = BooksExtra(existrev=bookInfo.checkExistRev(session["user_id"]),existlike=bookInfo.checkfirstlike(session["user_id"]),likecount=len(bookInfo.likes), avRate=avRate, rate=bookInfo.getOurAvRate())
        return  render_template("bookInfo.html",bookinfo=bookInfo,reviews=reviews,users=users, bookextra=bookextra)
    else:
        return  render_template("search.html")


@app.route("/addreview/<string:bookisbn>",methods=["GET","POST"])
def addreview(bookisbn):
    if session.get("user_id") is None:
        return  render_template("homepage.html")
    elif request.method=="POST":
        book = Book.query.get(bookisbn)
        rate = request.form.get("ratereview")
        content = request.form.get("reviewcontent")
        if rate == None:
            rate = 3
        book.add_Rev(user_id=session["user_id"],rate=int(rate),content=content)
        reviews = book.reviews
        avRate = book.getGoodreads()
        users = book.listofnames(reviews)
        bookextra = BooksExtra(existrev=book.checkExistRev(session["user_id"]),existlike=book.checkfirstlike(session["user_id"]),likecount=len(book.likes), avRate=avRate, rate=book.getOurAvRate())
        return  render_template("bookInfo.html",bookinfo=book,reviews=reviews,users=users, bookextra=bookextra)
    else:
        book = Book.query.get(bookisbn)
        if book.checkExistRev(session["user_id"]):
            reviews = book.reviews
            avRate = book.getGoodreads()
            users = book.listofnames(reviews)
            bookextra = BooksExtra(existrev=book.checkExistRev(session["user_id"]),existlike=book.checkfirstlike(session["user_id"]),likecount=len(book.likes), avRate=avRate, rate=book.getOurAvRate())
            return  render_template("bookInfo.html",bookinfo=book,reviews=reviews,users=users, bookextra=bookextra)
        else:
            return  render_template("addreview.html",bookisbn=bookisbn)


@app.route("/Addnewlike/<string:bookisbn>",methods=["GET"])
def Addnewlike(bookisbn):
        if session.get("user_id") is None:
            return  render_template("homepage.html")
        book = Book.query.get(bookisbn)
        book.addLike(session["user_id"])
        reviews = book.reviews
        avRate = book.getGoodreads()
        users = book.listofnames(reviews)
        bookextra = BooksExtra(existrev=book.checkExistRev(session["user_id"]),existlike=book.checkfirstlike(session["user_id"]),likecount=len(book.likes), avRate=avRate, rate=book.getOurAvRate())
        return  render_template("bookInfo.html",bookinfo=book,reviews=reviews,users=users, bookextra=bookextra)
