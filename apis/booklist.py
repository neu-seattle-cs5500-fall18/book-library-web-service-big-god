from flask import request
from flask_restplus import Namespace, Resource, reqparse

from .models import *
import json

api = Namespace('lists', description='BookLists related operations')

parser = reqparse.RequestParser()

# TODO: the "owner_id" parameter should be removed after logged in user info is saved
parser.add_argument('owner_id', help='id of the user who created the list')
parser.add_argument('list_name', help='name of the list')
parser.add_argument('books', action='append', help='books (represented as book_id) to be included in the list')

@api.route('/')
class Lists(Resource):

    @api.doc('get_lists')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @api.doc(params={'owner_id': 'user_id of the owner'})
    def get(self):
        '''get all lists created by a given user'''
        return 'Success', 200
    
    @api.doc('create_list')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.expect(parser)
    def post(self):
        '''create a list'''
        data = request.data
        data_dict = json.loads(data)
        new_list = List(ListName=data_dict['name'])
        db.session.add(new_list)
        db.session.commit()
        return "Success!", 201


@api.route('/<list_id>')
@api.param('list_id', 'The list identifier')
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
    @api.expect(parser)
    def put(self, list_id):
        '''update a list given its identifier'''
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
        '''delete a list given its identifier'''
        List.query.get_or_404(list_id)
        List.query.filter_by(ListId=list_id).delete()
        db.session.commit()
        return 'Success', 204