from flask import request
from flask_restplus import Namespace, Resource, reqparse

from .models import *
import json

api = Namespace('lists', description='BookLists related operations')

parser = reqparse.RequestParser()
parser.add_argument('list_name')
parser.add_argument('owner_id')


@api.route('/')
class Lists(Resource):

    @api.doc('get_lists')
    @api.expect(parser)
    def get(self):
        return 'Success', 200
    
    @api.doc('create_list')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_list = List(ListName=data_dict['name'])
        db.session.add(new_list)
        db.session.commit()
        return "Success!", 201


@api.route('/<list_id>')
@api.param('list', 'The list identifier')
@api.response(404, 'List not found')
class ListOfID(Resource):
    @api.doc(responses={
        200: 'Success',
    })
    @api.doc('get_list')
    def get(self, list_id):
        '''Fetch a list given its identifier'''
        return 'Success', 200

    @api.doc(responses={
        200: 'Success',
    })
    def put(self, list_id):
        data = request.data
        data_dict = json.loads(data)
        # books = data_dict['books']

        args = parser.parse_args()
        list_name = args['list_name']
        return {"update list": "success"}, 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, list_id):
        return 'Success', 204