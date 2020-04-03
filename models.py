import os

from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import requests

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    reviews = db.relationship("Review", backref="User", lazy=True)
    likes = db.relationship("Like", backref="User", lazy=True)


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    reviews = db.relationship("Review", backref="Book", lazy=True)
    likes = db.relationship("Like", backref="Book", lazy=True)

    def addLike(self, user_id):
        like = Like(user_id = user_id, book_isbn = self.isbn)
        db.session.add(like)
        db.session.commit()

    def add_Rev(self, user_id, rate, content):
        rev = Review(content=content,rate=rate,user_id=user_id,book_isbn=self.isbn)
        db.session.add(rev)
        db.session.commit()

    def checkExistRev(self, user_id):
        exist = False
        for rev in self.reviews:
            if rev.user_id == user_id:
                exist = True
        return exist

    def listofnames(self, reviews):
        users = []
        for review in reviews:
            userName = User.query.get(review.user_id)
            users.append(userName.username)
        return users

    def checkfirstlike(self, user_id):
        existlike = False
        for lik in self.likes:
            if lik.user_id == user_id:
                existlike = True
        return existlike

    def getGoodreads(self):
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "7c49zzVsGsbIkJX91bNmIw", "isbns": self.isbn})
        if res.status_code != 200:
            return "0"
        data = res.json()
        avRate = data["books"]
        for i in avRate:
            return i['average_rating']

    def getOurAvRate(self):
        count = 0
        sum = 0
        for review in self.reviews:
            count+=1
            sum = sum + review.rate
        if count == 0:
            return 0
        return sum/count



class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
