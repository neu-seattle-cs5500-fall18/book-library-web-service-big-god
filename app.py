from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, reqparse
from Model import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://szrznmfhslbepo:6fa44bfa2f7d22de2aa86cf0e8d5e134d5b753898cee8fe3fbeb609e741404c2@ec2-174-129-35-61.compute-1.amazonaws.com:5432/d4u32t92996vao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# initial with an application object
api = Api(app, version='1.0', title='Book Api', description='An Api for Books')

# request parser
parser = reqparse.RequestParser()

# create tables if not exist
with app.app_context():
    db.create_all()

@api.route('/hello')
class hello(Resource):
    parser.add_argument('world')
    def get(self):
        args = parser.parse_args()
        return {'world': args['world']}

# Post json format example:
# {
#   "userName": "sam123",
#   "passWord": "yes123"
# }


@api.route('/users')
class user(Resource):
    parser.add_argument('username')
    def get(self):
        userList = User.query.order_by(User.UserId).all()

        # returned list of User objects must be serialized
        return jsonify(Serializer.serialize_list(userList))

    def post(self):
        data = request.data
        dataDict = json.loads(data)
        newUser = User(UserName=dataDict['userName'], PassWord=dataDict['passWord'])
        db.session.add(newUser)
        db.session.commit()
        return "Success!"

    def delete(self):
        args = parser.parse_args()
        username = args['username']
        User.query.filter_by(UserName=username).delete()
        db.session.commit()
        return "Success!"

if __name__ == '__main__':
    app.run()
