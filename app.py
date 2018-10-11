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
parser.add_argument('bookID')
parser.add_argument('owner_id')
parser.add_argument('author_id')
parser.add_argument('year_start')
parser.add_argument('year_end')
parser.add_argument('genre')


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
#   "OwnerID" : 1,
#   "BookName" : "Harry Potter",
#   "PublishDate" : "1997",
#   "LoanedOut" : false
# }

@api.route('/books')
class books(Resource):

    # TODO: combine all get query in one function, need to refactor
    # it when the query become complicated

    def get(self):
        args = parser.parse_args()
        bookID = args['bookID']
        owner_id = args['owner_id']
        author_id = args['author_id']
        year_start = args['year_start']
        year_end = args['year_end']
        genre = args['genre']

        if bookID is not None:
            book = Book.query.get(bookID)
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
        newBook = Book(OwnerID=dataDict['ownerID'],
                       BookName=dataDict['bookName'],
                       PublishDate=dataDict['publishDate'],
                       LoanedOut=dataDict['loanedOut'])
        db.session.add(newBook)
        db.session.commit()
        return "Success!"

    def delete(self):
        args = parser.parse_args()
        bookID = args['bookID']
        Book.query.filter_by(BookID=bookID).delete()
        db.session.commit()
        return "Success!"

    def put(self):
        data = request.data
        dataDict = json.loads(data)

        args = parser.parse_args()
        bookID = args['bookID']
        book = Book.query.get(bookID)
        book.OwnerID = dataDict['ownerID']
        book.BookName = dataDict['bookName']
        book.PublishDate = dataDict['publishDate']
        book.LoanedOut = dataDict['loanedOut']
        db.session.commit()
        return "Success!"


if __name__ == '__main__':
    app.run()
