from flask import request, jsonify
from flask_restplus import Namespace, Resource, reqparse
from .models import *
import json

api = Namespace('lists', description='BookLists related operations')

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


# Post list json format example:
# {
#   "name": "sci",
# }
@api.route('/')
class Lists(Resource):
    @api.doc('create_list')
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_list = List(ListName=data_dict['name'])
        db.session.add(new_list)
        db.session.commit()
        return "Success!", 201

    @api.doc('update_list')
    def put(self):
        data = request.data
        data_dict = json.loads(data)
        # books = data_dict['books']

        args = parser.parse_args()
        list_name = args['list_name']
        return {"update list": "success"}
