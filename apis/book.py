from flask import jsonify, request
from flask_restplus import Namespace, Resource, reqparse
from . import models
import json

api = Namespace('books', description='Books related operations')

# request parser
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('book_id')
parser.add_argument('owner_id')
parser.add_argument('author_id')
parser.add_argument('year_start')
parser.add_argument('year_end')
parser.add_argument('genre')
parser.add_argument('list_name')
parser.add_argument('loan_id')
parser.add_argument('note_id')


@api.route('/')
class Books(Resource):
    # TODO 1: current logic combine all get queries in one function, need to refactor
    #         it when the query become complicated

    @api.doc('get_book')
    def get(self):
        args = parser.parse_args()
        book_id = args['book_id']
        owner_id = args['owner_id']
        author_id = args['author_id']
        year_start = args['year_start']
        year_end = args['year_end']
        genre = args['genre']

        if book_id is not None:
            book = models.Book.query.get(book_id)
            return jsonify(models.Serializer.serialize(book))

        if owner_id is not None:
            return {"books": "all books from owner"}
            # ownerBookList = Book.query.filter_by(OwnerID=owner_id)
            # return jsonify(Serializer.serialize_list(ownerBookList))

        if author_id is not None:
            return {"books": "all books from author"}

        if year_start is not None:
            return {"books": "all books from year_start to year_end"}

        if genre is not None:
            return {"books": "all books of genre"}

        # if no params pass in request url, return all books
        # TODO: remove this eventually, only for test
        book_list = models.Book.query.order_by(Book.BookID).all()
        return jsonify(models.Serializer.serialize_list(book_list))

    @api.doc('create_book')
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_book = Book(OwnerID=data_dict['owner_id'],
                        BookName=data_dict['title'],
                        PublishDate=data_dict['publish_date'],
                        LoanedOut=data_dict['loaned_out'])
        models.db.session.add(new_book)
        models.db.session.flush()

        if 'genres' in data_dict:
            for genre in data_dict['genres']:
                models.db.session.add(models.BookToGenres(BookId=new_book.BookID,
                                                          Genre=genre))

        if 'authors' in data_dict:
            for author in data_dict['authors']:
                names = author.split(" ")
                firstname = names[0]
                lastname = names[-1]
                new_author = models.Author(FirstName=firstname,
                                           LastName=lastname)
                models.db.session.add(new_author)
                models.db.session.flush()
                new_booktoauthors = models.BookToAuthors(BookId=new_book.BookID,
                                                         AutherID=new_author.AuthorID)
                models.db.session.add(new_booktoauthors)
                models.db.session.flush()
                models.db.session.commit()
        return "Success!"

    @api.doc('delete_book')
    def delete(self):
        args = parser.parse_args()
        book_id = args['book_id']
        models.BookToGenres.query.filter_by(BookId=book_id).delete()
        Book.query.filter_by(BookID=book_id).delete()
        models.db.session.commit()
        return "Success!"

    @api.doc('update_book')
    def put(self):
        data = request.data
        data_dict = json.loads(data)

        args = parser.parse_args()
        book_id = args['book_id']
        book = Book.query.get(book_id)
        book.OwnerID = data_dict['owner_id']
        book.BookName = data_dict['title']
        book.PublishDate = data_dict['publish_date']
        book.LoanedOut = data_dict['loaned_out']
        models.db.session.commit()
        return "Success!"


@api.route('/<id>')
@api.param('id', 'The book identifier')
@api.response(404, 'Book not found')
class Book(Resource):
    @api.doc('get_book')
    def get(self, id):
        '''Fetch a book given its identifier'''
        return models.Book.query.get_or_404(id)
