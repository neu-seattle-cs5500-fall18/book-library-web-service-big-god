from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, reqparse
from Model import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://szrznmfhslbepo:6fa44bfa2f7d22de2aa86cf0e8d5e134d5b753898cee8fe3fbeb609e741404c2@ec2-174-129-35-61.compute-1.amazonaws.com:5432/d4u32t92996vao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# initial with an application object
api = Api(app, version='1.0', title='Book Api', description='An Api for Books')

# request parser
parser = reqparse.RequestParser()
parser.add_argument('world')
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

# create tables if not exist
with app.app_context():
    db.create_all()

@api.route('/hello')
class hello(Resource):
    def get(self):
        args = parser.parse_args()
        return {'world': args['world']}

# Post json format example:
# {
#   "userName": "sam123",
#   "passWord": "yes123"
# }

@api.route('/users')
class users(Resource):
    def get(self):
        userList = User.query.order_by(User.UserId).all()

        # returned list of User objects must be serialized
        return jsonify(Serializer.serialize_list(userList))

    def post(self):
        data = request.data
        dataDict = json.loads(data)
        newUser = User(UserName=dataDict['userName'], PassWord=dataDict['passWord'])
        db.session.add(newUser)
        db.session.commit()
        return "Success!"

    def delete(self):
        args = parser.parse_args()
        username = args['username']
        User.query.filter_by(UserName=username).delete()
        db.session.commit()
        return "Success!"


# Post book json format example:
# {
#   "owner_id" : 1,
#   "title" : "Harry Potter",
#   "publish_date" : "1993-05-07 10:41:37",
# }

@api.route('/books')
class books(Resource):

    # TODO 1: current logic combine all get queries in one function, need to refactor
    # it when the query become complicated

    # TODO 2: implement all functions with real logic

    def get(self):
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
        bookList = Book.query.order_by(Book.BookID).all()
        return jsonify(Serializer.serialize_list(bookList))

    def post(self):
        data = request.data
        dataDict = json.loads(data)
        newBook = Book(OwnerID=dataDict['owner_id'],
                       BookName=dataDict['title'],
                       PublishDate=dataDict['publish_date'],
                       LoanedOut=dataDict['loaned_out'])
        db.session.add(newBook)
        db.session.commit()
        return "Success!"

    def delete(self):
        args = parser.parse_args()
        book_id = args['book_id']
        Book.query.filter_by(BookID=book_id).delete()
        db.session.commit()
        return "Success!"

    def put(self):
        data = request.data
        dataDict = json.loads(data)

        args = parser.parse_args()
        book_id = args['book_id']
        book = Book.query.get(book_id)
        book.OwnerID = dataDict['owner_id']
        book.BookName = dataDict['title']
        book.PublishDate = dataDict['publish_date']
        book.LoanedOut = dataDict['loaned_out']
        db.session.commit()
        return "Success!"

# Post list json format example:
# {
#   "name": "sci",
# }
@api.route('/lists')
class lists(Resource):
    def post(self):
        data = request.data
        dataDict = json.loads(data)
        newList = List(ListName=dataDict['name'])
        db.session.add(newList)
        db.session.commit()
        return "Success!"

    def put(self):
        data = request.data
        dataDict = json.loads(data)
        # books = dataDict['books']

        args = parser.parse_args()
        list_name = args['list_name']

        return {"update list": "success"}

# Post loan json format example:
# {
#   "book_id" : 1,
#   "borrower_id" : "1",
#   "due" : "1993-05-07 10:41:37",
# }
@api.route('/loans')
class loans(Resource):
    def post(self):
        data = request.data
        dataDict = json.loads(data)
        newLoanHistory = LoanHistory(BookId=dataDict['book_id'],
                                     BorrowerId=dataDict['borrower_id'],
                                     Due=dataDict['due'])
        db.session.add(newLoanHistory)
        db.session.commit()
        return "Success!"

    def put(self):
        data = request.data
        dataDict = json.loads(data)
        # return_date = dataDict['return_date']

        args = parser.parse_args()
        loan_id = args['loan_id']
        return {"update loan": "success"}

    def get(self):
        args = parser.parse_args()
        return {"get loan status": "return or not + return date"}


# Post note json format example:
# {
#   "book_id": book_id,
#   "note": string,
# }
@api.route('/notes')
@api.response(404, "Note not found")
class Notes(Resource):

    @api.doc('get_note')
    def get(self):
        args = parser.parse_args()
        note_id = args['note_id']
        note = Note.query.get(note_id)
        return jsonify(Serializer.serialize(note))

    @api.doc('create_note')
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_note = Note(BookId=data_dict['book_id'],
                       Content=data_dict['note'])
        db.session.add(new_note)
        db.session.commit()
        return "Success!", 201

    @api.doc('delete_note')
    def delete(self):
        args = parser.parse_args()
        note_id = args['note_id']
        Note.query.filter_by(NoteId=note_id).delete()
        db.session.commit()
        return "Success!"

    @api.doc('update_note')
    def put(self):
        data = request.data
        data_dict = json.loads(data)

        args = parser.parse_args()
        note_id = args['note_id']
        note = Note.query.get(note_id)
        note.Content = data_dict['note']
        db.session.commit()
        return "Success!"

if __name__ == '__main__':
    app.run()
