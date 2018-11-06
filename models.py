from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(80), unique=True, nullable=False)
    PassWord = db.Column(db.String(80), unique=False, nullable=False)
    
    def serialize(self):
        res = Serializer.serialize(self)
        return res


class Author(db.Model):
    AuthorId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), unique=False, nullable=False)
    LastName = db.Column(db.String(80), unique=False, nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


# class Genre(enum.Enum):
#     Science = 'Science'
#     Horror = 'Horror'

#     def serialize(self):
#         return repr(self)


class List(db.Model):
    ListId = db.Column(db.Integer, primary_key=True)
    ListName = db.Column(db.String(80), unique=False, nullable=False)
    OwnerId = db.Column(db.Integer, db.ForeignKey(User.UserId), unique=False, nullable=False)
    Created = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class Book(db.Model):
    BookId = db.Column(db.Integer, primary_key=True)
    OwnerId = db.Column(db.Integer, db.ForeignKey(User.UserId), nullable=False)
    BookName = db.Column(db.String(300), unique=False, nullable=False)
    PublishDate = db.Column(db.DateTime, unique=False, nullable=True)
    LoanedOut = db.Column(db.Boolean, unique=False, nullable=True)

    def serialize(self):
        res = {
            "BookId": self.BookId,
            "OwnerId": self.OwnerId,
            "BookName": self.BookName,
            "PublishDate": self.PublishDate.__str__(),
            "LoanedOut": self.LoanedOut,
        }
        return res


class Note(db.Model):
    NoteId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookId), nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey(User.UserId), nullable=False)
    Content = db.Column(db.String(300), unique=False, nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class LoanHistory(db.Model):
    LoanId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookId), nullable=False)
    BorrowerId = db.Column(db.Integer, db.ForeignKey(User.UserId), nullable=False)
    Due = db.Column(db.DateTime, unique=False, nullable=True)
    ActualReturnDate = db.Column(db.DateTime, unique=False, nullable=True)

    def serialize(self):
        res = {
            "LoanId": self.LoanId,
            "BookId": self.BookId,
            "BorrowerId": self.BorrowerId,
            "Due": self.Due.__str__(),
            "ActualReturnDate": self.ActualReturnDate.__str__(),
        }
        return res


class BookToAuthors(db.Model):
    BookToAuthorsMapId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookId), nullable=False)
    AuthorId = db.Column(db.Integer, db.ForeignKey(Author.AuthorId), nullable=False)
    __table_args__ = (db.UniqueConstraint('BookId', 'AuthorId', name='_book_author_uc'),)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class BookToGenres(db.Model):
    BookToGenresId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookId), nullable=False)
    Genre = db.Column(db.String(80))
    __table_args__ = (db.UniqueConstraint('BookId', 'Genre', name='_book_genre_uc'),)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class ListToBooks(db.Model):
    ListToBooks = db.Column(db.Integer, primary_key=True)
    ListId = db.Column(db.Integer, db.ForeignKey(List.ListId), nullable=False)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookId), nullable=False)
    __table_args__ = (db.UniqueConstraint('ListId', 'BookId', name='_list_book_uc'),)

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
