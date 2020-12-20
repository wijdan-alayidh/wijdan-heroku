import os
from datetime import datetime
from flask import Flask, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exc
import json
from flask_cors import CORS

from models import setup_db, db_drop_and_create_all, Actors, Movies
from auth.auth import AuthError, requires_auth

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
    @requires_auth('get:actors')
    def get_actors(jwt):

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
    @requires_auth('post:actors')
    def post_new_actors(jwt):

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
    @requires_auth('get:actors')
    def get_individual_actor(jwt,actor_id):

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
    @requires_auth('delete:actors')
    def delete_actor(jwt,actor_id):
        
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
    @requires_auth('patch:actors')
    def update_actor(jwt,actor_id):

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


    ''' ---- MOVIES Endpoints ----  '''

    ##  GET Endpoint to show the all available movies data
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        
        # import all available data about movies in database
        movies = Movies.query.all()
        # if no data available in database return --> 404 error
        if movies == []:
            return abort(404)

        # else return the data in the specific formate
        else:
            try:
                # because the database will return array this to get individual objects
                movie = [movie.format() for movie in movies]

                return jsonify({
                    'success': True,
                    'movies': movie
                })
            except:
                abort(422)

    ## POST Endpoint to insert new movie into the database
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(jwt):

        # get the json object form the request body
        body = request.get_json()
        # get the title and relased date from the body request
        title = body.get('title', None)
        relase_date = body.get('relase_date', None)

        try:
            # insert the data from request and try to insert new record in database
            movie = Movies(title=title, relase_date=relase_date)

            movie.insert()

            return jsonify({
                "success": True,
                "new movie": movie.format()
            })
        
        except:
            abort(422)

    ## GET Endpoint to show specific movie data 
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_individual_movie(jwt,movie_id):

        # get the data about the movie based on the movie id
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        
        # check if the requested movie is available
        # if is not available return --> 404 error 
        if movie == None:
            return abort(404)
    
        # else return all available data about movie
        else:
            try:
                return jsonify({
                    'success': True,
                    'movie': movie.format()
                })
            except:
                abort(422)
    
    ## DELETE Endpoint to delete movie from the database based on the movie id
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt,movie_id):

        # get the data about the movie based on the movie id
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        
        # check if the requested movie is available
        # if is not available return --> 404 error 
        if movie == None:
            return abort(404)
    
        # else delete the movie based on the movie id
        else:  
            try:
                movie.delete()

                return jsonify({
                    "success": True,
                    "Deleted Movie": movie.title
                })
            except:
                abort(422)

    ## PATCH Endpoint to update data of specific movie based on movie id
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt,movie_id):

        # get the data about the movie based on the movie id
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        
        # check if the requested movie is available
        # if is not available return --> 404 error 
        if movie == None:
            return abort(404)
        
        else:  
            # else get json body form the request   
            body = request.get_json()
            try:
                # update movie title
                if 'title' in body:
                    movie.title = body.get('title')
                
                # update movie relased date
                elif 'relase_date' in body:
                    movie.relase_date = body.get('relase_date')

                movie.update()

                return jsonify ({
                    "success": True,
                    "Movie Information": movie.format()
                })

            except:
                abort(422)

    ''' ---- Error Handlers ---- '''

    ##   Error Handlers for AuthError
    
    # - 401
    @app.errorhandler(AuthError)
    def unauthorized(AuthError):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthrized Access."
        }), 401

    # - 403
    @app.errorhandler(AuthError)
    def unauthorized(AuthError):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Access Denied."
        }), 403

    ##   Error Handlers for other expected errors
    # - 400
    @app.errorhandler(400)
    def bad_request(error):
            return jsonify({
                "success": False,
                "error": 400,
                "message": "Bad Request."
            }), 400

    # - 404
    @app.errorhandler(404)
    def not_found(error):
            return jsonify({
                "success": False,
                "error": 404,
                "message": "Resource Not Found."
            }), 404
    
    # - 405
    @app.errorhandler(405)
    def not_allowed(error):
            return jsonify({
                "success": False,
                "error": 405,
                "message": "Method Not Allowed."
            }), 405
    
    # - 422
    @app.errorhandler(422)
    def unprocessable(error):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Unprocessable."
            }), 422
    
    # - 500
    @app.errorhandler(500)
    def internal_server_error(error):
            return jsonify({
                "success": False,
                "error": 500,
                "message": "Internal Server Error."
            }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()


