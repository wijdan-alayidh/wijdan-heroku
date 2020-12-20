import os
from datetime import datetime
from flask import Flask, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exc
import json
from flask_cors import CORS

from models import setup_db, db_drop_and_create_all, Actors, Movies
# from auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    ''' ----- Basic App Configuration ----- '''
    
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    db_drop_and_create_all()

    @app.route('/', methods=['GET'])
    def main_page():
        
        return "Welcome to our app"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()