from flask import request
from flask_restplus import Namespace, Resource

from apis.utils import lists_parser as parser
from .models import *
import json

api = Namespace('lists', description='BookLists related operations')


@api.route('/')
class Lists(Resource):
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

    @api.doc('update_list')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def put(self):
        data = request.data
        data_dict = json.loads(data)
        # books = data_dict['books']

        args = parser.parse_args()
        list_name = args['list_name']
        return {"update list": "success"}, 200
