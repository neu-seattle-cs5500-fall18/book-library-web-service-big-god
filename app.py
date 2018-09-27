from flask import Flask

app = Flask(__name__)

# Connect to database
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

@app.route('/')
def hello():
    return "Hello there"



