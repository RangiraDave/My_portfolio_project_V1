from flask import Flask

# app = Flask(__name__)

def create_app():
    app =Flask(__name__)

    
    from . import routes  # Import inside function to avoid circular import
    return app
