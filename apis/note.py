from flask import jsonify, request
from flask_restplus import Namespace, Resource, reqparse

from .models import *
import json

api = Namespace('notes', description='Notes related operations')

parser = reqparse.RequestParser()
parser.add_argument('book_id')
parser.add_argument('user_id')


# Post note json format example:
# {
#   "book_id": book_id,
#   "note": string,
# }
@api.route('/')
@api.response(400, 'Validation Error')
class Notes(Resource):

    @api.doc('get_notes')
    @api.doc(responses={
        200: 'Success',
    })
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        book_id = args['book_id']
        user_id = args['user_id']
        # TODO: add logic to find by book_id and/or user_id
        note_list = Note.query.order_by(Note.NoteId).all()
        return Serializer.serialize(note_list), 200

    @api.doc('create_note')
    @api.doc(responses={
        201: 'Created',
    })
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        new_note = Note(BookId=data_dict['book_id'],
                        UserId=data_dict['user_id'])
        db.session.add(new_note)
        db.session.commit()
        return new_note.serialize(), 201


@api.route('/<note_id>')
@api.param('note_id', 'The note identifier')
@api.response(404, 'Note not found')
class NoteOfID(Resource):
    @api.doc(responses={
        200: 'Success',
    })
    @api.doc('get_note')
    def get(self, note_id):
        '''Fetch a note given its identifier'''
        note = Note.query.get_or_404(note_id)
        return note.serialize(), 200

    @api.doc(responses={
        200: 'Success',
    })
    @api.doc(params={'content': 'The note content'})
    def put(self, note_id):
        '''Update the content of a note given its identifier'''
        note = Note.query.get_or_404(note_id)
        args = parser.parse_args()
        content = args['content']
        if content is not None:
            note.Content = content
        db.session.commit()
        return note.serialize(), 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, note_id):
        '''Delete a note given its identifier'''
        Note.query.get_or_404(note_id)
        Note.query.filter_by(NoteId=note_id).delete()
        db.session.commit()
        return 'Success', 204
