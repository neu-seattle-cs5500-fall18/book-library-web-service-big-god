from flask import jsonify, request
from flask_restplus import Namespace, Resource

from apis.utils import notes_parser as parser
from .models import *
import json

api = Namespace('notes', description='Notes related operations')


# Post note json format example:
# {
#   "book_id": book_id,
#   "note": string,
# }
@api.route('/')
class Notes(Resource):

    @api.doc('get_note')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def get(self):
        args = parser.parse_args()
        note_id = args['note_id']
        note = Note.query.get(note_id)
        response = jsonify(Serializer.serialize(note))
        response.status_code = 200
        return response

    @api.doc('create_note')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_note = Note(BookId=data_dict['book_id'],
                        Content=data_dict['note'])
        db.session.add(new_note)
        db.session.commit()
        return "Success!", 201

    @api.doc('delete_note')
    @api.doc(responses={
        204: 'Deleted',
        400: 'Validation Error'
    })
    def delete(self):
        args = parser.parse_args()
        note_id = args['note_id']
        Note.query.filter_by(NoteId=note_id).delete()
        db.session.commit()
        return "Success!", 204

    @api.doc('update_note')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def put(self):
        data = request.data
        data_dict = json.loads(data)

        args = parser.parse_args()
        note_id = args['note_id']
        note = Note.query.get(note_id)
        note.Content = data_dict['note']
        db.session.commit()
        return "Success!", 200
