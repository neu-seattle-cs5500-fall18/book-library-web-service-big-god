from urllib import response

from flask import jsonify, request
from flask_restplus import Namespace, Resource, reqparse

from apis.models import *

api = Namespace('books', description='Books related operations')

# Add more arguments if needed
parser = reqparse.RequestParser()
parser.add_argument('owner_id', help='The user_id of the owner')
parser.add_argument('title', help='The title of the book')
parser.add_argument('author_id', help='The id of the author')
parser.add_argument('year_start', help='Find books that published after some year')
parser.add_argument('year_end', help='Find books that published before some year')
parser.add_argument('genres', help='The genre that the books belong to')
parser.add_argument('list_name', help='The list name that the books belong to')
parser.add_argument('loaned_out', help='Boolean if the book is loaned out')
parser.add_argument('publish_date', help='The publish date of book')


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
        owner_id = args['owner_id']
        author_id = args['author_id']
        title = args['title']
        year_start = args['year_start']
        year_end = args['year_end']
        genres = args['genres']

        if owner_id is not None:
            return {"books": "all books from owner"}
            # ownerBookList = Book.query.filter_by(OwnerID=owner_id)
            # return jsonify(Serializer.serialize_list(ownerBookList))

        if author_id is not None:
            return {"books": "all books from author"}

        if year_start is not None:
            return {"books": "all books from year_start to year_end"}

        if genres is not None:
            return {"books": "all books of genres"}

        # if no params pass in request url, return all books
        # TODO: remove this eventually, only for test
        book_list = Book.query.order_by(Book.BookId).all()
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
        args = parser.parse_args()
        new_book = Book(OwnerId=args['owner_id'],
                        BookName=args['title'])
        db.session.add(new_book)
        db.session.flush()
        db.session.commit()

        # if 'genres' in args:
        #     #for genre in args['genres']:
        #     a = args['genres']
        #     db.session.add(BookToGenres(BookId=new_book.BookId,
        #                                 Genre=Genre[a]))
        #     db.session.flush()
        #     db.session.commit()
        #
        # if 'authors' in args:
        #     for author in args['authors']:
        #         names = author.split(" ")
        #         firstname = names[0]
        #         lastname = names[-1]
        #         new_author = Author(FirstName=firstname,
        #                             LastName=lastname)
        #         db.session.add(new_author)
        #         db.session.flush()
        #         new_booktoauthors = BookToAuthors(BookId=new_book.BookID,
        #                                           AutherID=new_author.AuthorID)
        #         db.session.add(new_booktoauthors)
        #         db.session.flush()
        #         db.session.commit()
        return new_book.serialize(), 201


@api.route('/<book_id>')
@api.param('book_id', 'The book identifier')
@api.response(404, 'Book not found')
class BookOfID(Resource):
    @api.doc(responses={
        200: 'Success',
    })
    @api.doc('get_book')
    def get(self, book_id):
        '''Fetch a book given its identifier'''
        book = Book.query.get_or_404(book_id)
        return book.serialize(), 200

    @api.doc(responses={
        200: 'Success',
    })
    @api.doc(params={'title': 'The book title',
                     'publish_date': 'The publication date',
                     'loaned_out': 'True if the book is loaned out'})
    def put(self, book_id):
        '''Update the information of a book given its identifier'''
        book = Book.query.get_or_404(book_id)
        args = parser.parse_args()
        title = args['title']
        publish_date = args['publish_date']
        loaned_out = args['loaned_out']
        if title is not None:
            book.BookName = title
        if publish_date is not None:
            book.PublishDate = publish_date
        if loaned_out is not None:
            book.LoanedOut = loaned_out
        # for genres or authors or lists, use the map classes
        db.session.commit()
        return book.serialize(), 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, book_id):
        '''Delete a book given its identifier'''
        Book.query.get_or_404(book_id)
        Book.query.filter_by(BookId=book_id).delete()
        db.session.commit()
        return 'Success', 204
