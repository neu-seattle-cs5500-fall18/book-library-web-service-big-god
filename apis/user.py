from flask import request, jsonify
from flask_restplus import Namespace, Resource, reqparse
from . import models
import json

api = Namespace('users', description='Users related operations')

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
class Users(Resource):
    @api.doc('get_user')
    def get(self):
        user_list = models.User.query.order_by(models.User.UserId).all()

        # returned list of User objects must be serialized
        return jsonify(models.Serializer.serialize_list(user_list))

    @api.doc('create_user')
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_user = User(UserName=data_dict['userName'],
                        PassWord=data_dict['passWord'])
        models.db.session.add(new_user)
        models.db.session.commit()
        return "Success!", 201

    @api.doc('delete_user')
    def delete(self):
        args = parser.parse_args()
        username = args['username']
        models.User.query.filter_by(UserName=username).delete()
        models.db.session.commit()
        return "Success!"


@api.route('/<id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    def get(self, id):
        '''Fetch a user given its identifier'''
        return models.User.query.get_or_404(id)
