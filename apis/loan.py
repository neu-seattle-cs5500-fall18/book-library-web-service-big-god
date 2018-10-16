from flask import request
from flask_restplus import Namespace, Resource, reqparse

from .models import *
import json

api = Namespace('loans', description='Loans related operations')

parser = reqparse.RequestParser()
parser.add_argument('book_id', help='The identifier of the book loaned out')
parser.add_argument('owner_id', help='The user_id of the owner of the book')
parser.add_argument('due', help='The due date of the book')
parser.add_argument('actual_return_date', help='The acturn return date of the book')


@api.route('/')
class Loans(Resource):
    @api.doc('create_loan')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.expect(parser)
    def post(self):
        '''create a loan'''
        data = request.data
        data_dict = json.loads(data)
        new_loan_history = LoanHistory(BookId=data_dict['book_id'],
                                       BorrowerId=data_dict['borrower_id'],
                                       Due=data_dict['due'])
        db.session.add(new_loan_history)
        db.session.commit()
        return "Success!", 201

    @api.doc('get_loan')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @api.doc(params={'owner_id': 'user_id of the owner'})
    def get(self): 
        '''get all loans created by a given user'''
        args = parser.parse_args()
        return {"get loan status": "return or not + return date"}, 200


@api.route('/<loan_id>')
@api.param('loan_id', 'The loan identifier')
@api.response(404, 'Note not found')
class LoanOfID(Resource):
    @api.doc(responses={
        200: 'Success',
    })
    @api.doc('get_loan')
    def get(self, loan_id):
        '''Fetch a loan given its identifier'''
        return 'Success', 200

    @api.doc(responses={
        200: 'Success',
    })

    @api.expect(parser)
    def put(self, loan_id):
        '''Update the content of a note given its identifier'''
        return 'Success', 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, loan_id):
        '''Delete a note given its identifier'''
        return 'Success', 204
