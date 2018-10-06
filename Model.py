from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

db = SQLAlchemy()

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    passWord = db.Column(db.String(80), unique=False, nullable=False)
    
    def serialize(self):
        res = Serializer.serialize(self)
        return res

class Author(db.Model):
    AutherID = db.Column(db.Integer, primary_key=True)
    AutherName = db.Column(db.String(80), unique=False, nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    BookName = db.Column(db.String(80), unique=False, nullable=False)
    AutherID = db.Column(db.Integer, db.ForeignKey('Author.AutherID'),nullable=False)
    OwnerID = db.Column(db.Integer, db.ForeignKey('User.userId'),nullable=False)
    PublishDate = db.Column(db.DateTime, unique=False, nullable=False)
    GenreType = db.Column(db.String(80), unique=False, nullable=False)
    LoanedOut = db.Column(db.Boolean, unique=False, nullable=False)
    LoanedUserID = db.Column(db.Integer, unique=False, nullable=True)
    ExpectedReturnDate = db.Column(db.DateTime, unique=False, nullable=True)
    ActualReturnDate = db.Column(db.DateTime, unique=False, nullable=True)
    Note = db.Column(db.String(300), unique=False, nullable=True)

    def serialize(self):
        res = Serializer.serialize(self)
        return res

# Serializer that converts class objects to json
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]