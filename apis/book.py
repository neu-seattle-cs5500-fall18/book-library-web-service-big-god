from flask import jsonify, request
from flask_restplus import Namespace, Resource

from apis.utils import books_parser as parser
from apis.models import *
import json

api = Namespace('books', description='Books related operations')


@api.route('/')
class Books(Resource):
    # TODO 1: current logic combine all get queries in one function, need to refactor
    #         it when the query become complicated
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @api.doc('get_books')
    @api.expect(parser)
    def get(self):
        '''Fetch books given constraints'''
        args = parser.parse_args()
        book_id = args['book_id']
        owner_id = args['owner_id']
        author_id = args['author_id']
        year_start = args['year_start']
        year_end = args['year_end']
        genre = args['genre']

        if book_id is not None:
            book = Book.query.get(book_id)
            return jsonify(Serializer.serialize(book))

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
        book_list = Book.query.order_by(Book.BookID).all()
        response = jsonify(Serializer.serialize_list(book_list))
        response.status_code = 200
        return response

    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.doc('create_book')
    @api.doc(params={'title': 'The book title',
                     'owner_id': 'The user_id of the owner'})
    def post(self):
        '''Add a new book to library'''
        data = request.data
        data_dict = json.loads(data)
        new_book = Book(OwnerID=data_dict['owner_id'],
                        BookName=data_dict['title'],
                        PublishDate=data_dict['publish_date'],
                        LoanedOut=data_dict['loaned_out'])
        db.session.add(new_book)
        db.session.flush()

        if 'genres' in data_dict:
            for genre in data_dict['genres']:
                db.session.add(BookToGenres(BookId=new_book.BookID,
                                            Genre=genre))

        if 'authors' in data_dict:
            for author in data_dict['authors']:
                names = author.split(" ")
                firstname = names[0]
                lastname = names[-1]
                new_author = Author(FirstName=firstname,
                                    LastName=lastname)
                db.session.add(new_author)
                db.session.flush()
                new_booktoauthors = BookToAuthors(BookId=new_book.BookID,
                                                  AutherID=new_author.AuthorID)
                db.session.add(new_booktoauthors)
                db.session.flush()
                db.session.commit()
        response = jsonify(new_book)
        response.status_code = 201
        return response


@api.route('/<id>')
@api.param('id', 'The book identifier')
@api.response(404, 'Book not found')
class BookOfID(Resource):
    @api.doc(responses={
        200: 'Success',
        404: 'Not Found'
    })
    @api.doc('get_book')
    def get(self, id):
        '''Fetch a book given its identifier'''
        return Book.query.get_or_404(id)

    @api.doc(responses={
        200: 'Success',
        404: 'Not Found'
    })
    @api.doc(params={'title': 'The book title',
                     'publish_date': 'The publication date',
                     'loaned_out': 'True if the book is loaned out'})
    def put(self, id):
        '''Update the information of a book given its identifier'''
        data = request.data
        data_dict = json.loads(data)
        book = Book.query.get(id)
        book.BookName = data_dict['title']
        book.PublishDate = data_dict['publish_date']
        book.LoanedOut = data_dict['loaned_out']
        db.session.commit()
        return 'Success', 200

    @api.doc(responses={
        204: 'Deleted',
        404: 'Not Found'
    })
    def delete(self, id):
        '''Delete a book given its identifier'''
        return 'Success', 204
