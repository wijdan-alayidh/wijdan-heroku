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

    @app.route('/',methods=['GET'])
    def main_page():
        
        return "Welcome to our app"


    ''' ----- ACTORS Endpoints ------ '''


    ## GET Endpoint to show all actors data
    @app.route('/actors', methods=['GET'])
    # @requires_auth('get:actors')
    # def get_actors(jwt):
    def get_actors():

        actors = Actors.query.all()

        # check if the query get a result from database
        # if not get a result --> return 404 error        
        if actors == []:
            abort(404)
        
        # else return all available data about actors
        else:
            try:
                actor = [actor.format() for actor in actors]
                return jsonify({
                        'success': True,
                        'actors': actor
                    })
            except:
                abort(422)

    ## POST Endpoint to post new actor into database
    @app.route('/actors', methods=['POST'])
    # @requires_auth('post:actors')
    # def post_new_actors(jwt):
    def post_new_actors():

        # At first get the json body from request
        body = request.get_json()

        # Then get the data needed to insert new actor (name and age and gender)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None).lower()

        # last step insert the new actor as new recorde in the database 
        try:
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                "success" : True,
                "new actor": actor.format()
            })

        except:
            abort(422)

    ## GET Endpoint to show specific actor data 
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    # @requires_auth('get:actors')
    def get_individual_actor(actor_id):
    # def get_individual_actor(jwt,actor_id):

        # get the data about the actor based on the actor id
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        # check if the requested actor is available
        # if is not available return --> 404 error 
        if actor == None:
            return abort(404)

        # else return the data availabe in database about the actor
        else:
            try:
                return jsonify({
                    'success': True,
                    'Actor': actor.format()
                })
            except:
                abort(422)

    ## DELETE Endpoint to delete actor from the database based on the actor id
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    # @requires_auth('delete:actors')
    # def delete_actor(jwt,actor_id):
    def delete_actor(actor_id):
        
        # get the data about the actor based on the actor id
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        # check if the requested actor is available
        # if is not available return --> 404 error 
        if actor == None:
            return abort(404)

        # else delete the actor based on the actor id
        else:
            try:
                actor.delete()

                return jsonify({
                    "success": True,
                    "Deleted Actor": actor.name
                })
            except:
                abort(422)

    ## PATCH Endpoint to update data of specific actor based on actor id
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    # @requires_auth('patch:actors')
    # def update_actor(jwt,actor_id):
    def update_actor(actor_id):

        # get the data about the actor based on the actor id
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        # check if the requested actor is available
        # if is not available return --> 404 error 
        if actor == None:
            return abort(404)

        
        else:
            # else get json body form the request
            body = request.get_json()
            try:
                # update actor name
                if 'name' in body:
                    actor.name = body.get('name')
                
                # update actor age
                elif 'age' in body:
                    actor.age = body.get('age')

                # update actor gender
                elif 'gender' in body:
                    actor.gender = body.get('gender')

                actor.update()

                return jsonify ({
                    "success": True,
                    "Actor Information": actor.format()
                })

            except:
                abort(422)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()


