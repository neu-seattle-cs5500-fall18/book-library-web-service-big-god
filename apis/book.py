from flask_restplus import Namespace, Resource, reqparse

from models import *

api = Namespace('books', description='Books related operations')

# Add more arguments if needed
parser = reqparse.RequestParser()
parser.add_argument('owner_id', help='The user_id of the owner')
parser.add_argument('title', help='The title of the book')
parser.add_argument('authors', action='append', help='The authors of the book')
parser.add_argument('year_start', help='Find books that published after some year')
parser.add_argument('year_end', help='Find books that published before some year')
parser.add_argument('genres', action='append', help='The genre that the books belong to')
parser.add_argument('list_name', help='The list name that the books belong to')
parser.add_argument('loaned_out', help='Boolean if the book is loaned out')
parser.add_argument('publish_date', help='The publish date of book')


@api.route('/')
class Books(Resource):
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
        author_id = args['authors']
        title = args['title']
        year_start = args['year_start']
        year_end = args['year_end']
        genres = args['genres']

        queries = []

        if owner_id is not None:
            queries.append(Book.OwnerId == owner_id)

        if title is not None:
            queries.append(Book.BookName == title)

        if year_start is not None:
            queries.append(Book.PublishDate >= year_start)

        if year_end is not None:
            queries.append(Book.PublishDate <= year_end)

        if author_id is not None:
            queries.append(Author.AuthorId.in_(author_id))

        if genres is not None:
            queries.append(BookToGenres.Genre.in_(genres))

        book_list = db.session.query(Book, BookToAuthors, Author, BookToGenres) \
            .join(BookToAuthors, Book.BookId == BookToAuthors.BookId) \
            .join(Author, Author.AuthorId == BookToAuthors.AuthorId) \
            .join(BookToGenres, BookToGenres.BookId == Book.BookId) \
            .filter(*queries).order_by(Book.BookId).all()

        ret_list = []

        # query returns list of books, need to parse the fields of each book
        for book in book_list:
            fields = {}

            for field in Serializer.serialize_list(book):
                for k, v in field.items():
                    if k not in fields:
                        fields[k] = v

            ret_list.append(fields)

        return ret_list, 200

    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.doc('create_book')
    # @api.doc(params={'title': 'The book title',
    #                  'owner_id': 'The user_id of the owner'})
    @api.expect(parser)
    def post(self):
        '''Add a new book to library'''
        args = parser.parse_args()
        new_book = Book(OwnerId=args['owner_id'],
                        BookName=args['title'])
        db.session.add(new_book)
        db.session.flush()
        db.session.commit()

        print('genres' in args)
        if args['genres'] is not None:
            for genre in args['genres']:
                # print(genre)
                db.session.add(BookToGenres(BookId=new_book.BookId,
                                            Genre=genre))
                db.session.flush()
            db.session.commit()
        else:
                db.session.add(BookToGenres(BookId=new_book.BookId,
                                            Genre=''))
                db.session.flush()
                db.session.commit()

        if args['authors'] is not None:
            for author in args['authors']:
                # print(author)
                names = author.split(" ")
                firstname = names[0]
                lastname = names[-1]
                new_author = Author(FirstName=firstname,
                                    LastName=lastname)
                db.session.add(new_author)
                db.session.flush()
                new_booktoauthors = BookToAuthors(BookId=new_book.BookId,
                                                  AuthorId=new_author.AuthorId)
                db.session.add(new_booktoauthors)
                db.session.flush()
                db.session.commit()
        else:
                new_author = Author(FirstName='',
                                    LastName='')
                db.session.add(new_author)
                db.session.flush()
                new_booktoauthors = BookToAuthors(BookId=new_book.BookId,
                                                  AuthorId=new_author.AuthorId)
                db.session.add(new_booktoauthors)
                db.session.flush()
                db.session.commit()
                
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
        # book = Book.query.get_or_404(book_id)

        book_list = db.session.query(Book, BookToAuthors, Author, BookToGenres) \
            .join(BookToAuthors, Book.BookId == BookToAuthors.BookId) \
            .join(Author, Author.AuthorId == BookToAuthors.AuthorId) \
            .join(BookToGenres, BookToGenres.BookId == Book.BookId) \
            .filter_by(BookId=book_id).order_by(Book.BookId).all()

        ret_list = []

        # query returns list of books, need to parse the fields of each book
        for book in book_list:
            fields = {}

            for field in Serializer.serialize_list(book):
                for k, v in field.items():
                    if k not in fields:
                        fields[k] = v

            ret_list.append(fields)

        return ret_list[0], 200

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
        BookToAuthors.query.filter_by(BookId=book_id).delete()
        BookToGenres.query.filter_by(BookId=book_id).delete()
        Book.query.filter_by(BookId=book_id).delete()
        db.session.commit()
        return 'Success', 204
