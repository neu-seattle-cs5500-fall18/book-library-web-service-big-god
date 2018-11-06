from flask import Flask

from apis import api
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://szrznmfhslbepo:6fa44bfa2f7d22de2aa86cf0e8d5e134d5b753898cee8fe3fbeb609e741404c2@ec2-174-129-35-61.compute-1.amazonaws.com:5432/d4u32t92996vao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# create tables if not exist
with app.app_context():
    db.create_all()

api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)

#
# # only for the purpose of testing
# @api.route('/booktogenres')
# class BookToGeneres(Resource):
#     def get(self):
#         list = BookToGenres.query.order_by(BookToGenres.BookToGenresId).all()
#
#         # returned list of User objects must be serialized
#         return list
#
#
# @api.route('/booktoauthors')
# class BookToAuthors(Resource):
#     def get(self):
#         list = BookToAuthors.query.order_by(BookToAuthors.BookToAuthorsMapId).all()
#
#         # returned list of User objects must be serialized
#         return jsonify(Serializer.serialize_list(list))

