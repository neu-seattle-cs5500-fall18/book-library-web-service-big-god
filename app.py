from flask import Flask
git
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello there"



