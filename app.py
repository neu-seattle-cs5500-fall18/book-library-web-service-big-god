from flask import Flask, request, jsonify
from Model import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://szrznmfhslbepo:6fa44bfa2f7d22de2aa86cf0e8d5e134d5b753898cee8fe3fbeb609e741404c2@ec2-174-129-35-61.compute-1.amazonaws.com:5432/d4u32t92996vao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# create tables if not exist
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return "Hello there"

# Post json format example:
# {
#   "userName": "sam123",
#   "passWord": "yes123"
# }

@app.route('/addUser', methods = ['POST'])
def addUser():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        newUser = User(userName=dataDict['userName'], passWord=dataDict['passWord'])
        db.session.add(newUser)
        db.session.commit()
        return "Success!"

@app.route('/getUser', methods = ['GET'])
def getUser():
    if request.method == 'GET':
        userList = User.query.order_by(User.userId).all()

        # returned list of User objects must be serialized
        return jsonify(Serializer.serialize_list(userList))

@app.route('/deleteUser/<userName>', methods = ['DELETE'])
def deleteUser(userName):
    if request.method == 'DELETE':
        User.query.filter_by(userName=userName).delete()
        db.session.commit()
        
        return "Success!"

if __name__ == '__main__':
    app.run()
