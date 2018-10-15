from flask import jsonify, request
from flask_restplus import Namespace, Resource, reqparse
from .models import *
import json

api = Namespace('notes', description='Notes related operations')

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


# Post note json format example:
# {
#   "book_id": book_id,
#   "note": string,
# }
@api.route('/')
class Notes(Resource):

    @api.doc('get_note')
    def get(self):
        args = parser.parse_args()
        note_id = args['note_id']
        note = Note.query.get(note_id)
        return jsonify(Serializer.serialize(note))

    @api.doc('create_note')
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_note = Note(BookId=data_dict['book_id'],
                        Content=data_dict['note'])
        db.session.add(new_note)
        db.session.commit()
        return "Success!", 201

    @api.doc('delete_note')
    def delete(self):
        args = parser.parse_args()
        note_id = args['note_id']
        Note.query.filter_by(NoteId=note_id).delete()
        db.session.commit()
        return "Success!"

    @api.doc('update_note')
    def put(self):
        data = request.data
        data_dict = json.loads(data)

        args = parser.parse_args()
        note_id = args['note_id']
        note = Note.query.get(note_id)
        note.Content = data_dict['note']
        db.session.commit()
        return "Success!"
