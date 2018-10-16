from flask import request, jsonify
from flask_restplus import Namespace, Resource

from apis.utils import users_parser as parser
from apis.models import *
import json

api = Namespace('users', description='Users related operations')


@api.route('/')
class Users(Resource):
    @api.doc('get_users')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def get(self):
        '''Fetch all users'''
        user_list = User.query.order_by(User.UserId).all()

        # returned list of User objects must be serialized
        response = jsonify(Serializer.serialize_list(user_list))
        response.status_code = 200
        return response

    @api.doc('create_user')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.doc(params={'username': 'The username',
                     'password': 'The password'})
    def post(self):
        '''Create a new user'''
        data = request.data
        data_dict = json.loads(data)
        new_user = User(UserName=data_dict['username'],
                        PassWord=data_dict['password'])
        db.session.add(new_user)
        db.session.commit()
        return "Success!", 201


@api.route('/<id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
class UserOfID(Resource):
    @api.doc('get_user')
    @api.doc(responses={
        200: 'Success',
        404: 'Not Found'
    })
    def get(self, id):
        '''Fetch a user given its identifier'''
        return User.query.get_or_404(id)

    @api.doc(responses={
        200: 'Success',
        404: 'Not Found'
    })
    @api.doc(params={'username': 'The username',
                     'password': 'The password'})
    def put(self, id):
        '''Update the information of a user given its identifier'''
        data = request.data
        data_dict = json.loads(data)
        user = User.query.get(id)
        user.UserName = data_dict['username']
        user.PassWord = data_dict['password']
        db.session.commit()
        return 'Success', 200

    @api.doc(responses={
        204: 'Deleted',
        404: 'Not Found'
    })
    def delete(self, id):
        '''Delete an user given its identifier'''
        return 'Success', 204
