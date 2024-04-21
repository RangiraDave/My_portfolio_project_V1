from flask import Flask
from app import routes, models
app = Flask(__name__)

@app.route('/')
def hello():
    return '<em>Hello, World!</em>'


if __name__ == '__main__':
    app.run()