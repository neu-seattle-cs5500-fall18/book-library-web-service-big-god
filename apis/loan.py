from flask import request
from flask_restplus import Namespace, Resource, reqparse

from .models import *
import json

api = Namespace('loans', description='Loans related operations')

parser = reqparse.RequestParser()
parser.add_argument('book_id')
parser.add_argument('user_id')


# Post loan json format example:
# {
#   "book_id" : 1,
#   "borrower_id" : "1",
#   "due" : "1993-05-07 10:41:37",
# }
@api.route('/')
class Loans(Resource):
    @api.doc('create_loan')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_loan_history = LoanHistory(BookId=data_dict['book_id'],
                                       BorrowerId=data_dict['borrower_id'],
                                       Due=data_dict['due'])
        db.session.add(new_loan_history)
        db.session.commit()
        return "Success!", 201

    @api.doc('update_loan')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def put(self):
        data = request.data
        data_dict = json.loads(data)
        # return_date = data_dict['return_date']

        args = parser.parse_args()
        loan_id = args['loan_id']
        return {"update loan": "success"}, 200

    @api.doc('get_loan')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def get(self):
        args = parser.parse_args()
        return {"get loan status": "return or not + return date"}, 200
