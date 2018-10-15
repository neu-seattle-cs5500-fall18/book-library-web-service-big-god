from flask import request
from flask_restplus import Namespace, Resource, reqparse
from .models import *
import json

api = Namespace('loans', description='Loans related operations')

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


# Post loan json format example:
# {
#   "book_id" : 1,
#   "borrower_id" : "1",
#   "due" : "1993-05-07 10:41:37",
# }
@api.route('/')
class Loans(Resource):
    @api.doc('create_loan')
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
    def put(self):
        data = request.data
        data_dict = json.loads(data)
        # return_date = data_dict['return_date']

        args = parser.parse_args()
        loan_id = args['loan_id']
        return {"update loan": "success"}

    @api.doc('get_loan')
    def get(self):
        args = parser.parse_args()
        return {"get loan status": "return or not + return date"}
