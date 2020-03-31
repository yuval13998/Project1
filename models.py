import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    year = db.Column(db.Integer, nullable=False)
    reviews = db.relationship("Review", backref="Book", lazy=True)
    likes = db.relationship("Like", backref="Book", lazy=True)

    def addLike(self, user_id):
        like = Like(user_id = user_id, book_isbn = self.isbn)
        db.session.add(like)
        db.session.commit()

    def addRev(self, user_id, rate, content):
        rev = Review(content=content,rate=rate,user_id=user_id,book_isbn=self.isbn)
        db.session.add(rev)
        db.session.commit()


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
