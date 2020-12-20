import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 

from app import create_app
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth

# This class represents the movies app test case
class MoviesTestCase(unittest.TestCase):

    # Define test variables and initialize app
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movies"
        self.database_path = "postgres://{}/{}".format('localhost:5432',  self.database_name)
        setup_db(self.app, self.database_path)
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.actor = {
            'name': 'actor name',
            'age': 26,
            'gender': 'female'
        }

        self.movie = {
            'title': "new movie title",
            'relased_date': "02-02-20202"
        }

    def tearDown(self):
        # excuted after reach test
        pass

    
    ''' ACTORS Tests '''

    # GET actors -- Success
    def test_actors(self):
        
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    # GET actors -- Failure
    def test_actors_not_found(self):
        
        res = self.client().get('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found.')

    # DELETE actor -- Success
    def test_delete_actor(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE actor -- Failure
    def test_delete_not_found_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found.')

    # POST actor -- Success
    def test_post_actor(self):
        res = self.client().post('/actors' , json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new actor'])

    # POST actor -- Failure
    def test_405_post_actor(self):
        res = self.client().post('/actors/1000' , json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed.")

    # PATCH actor -- Success
    def test_update_actor(self):
        res = self.client().patch('actors/1', json={'name': "new actor name"})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['name'], "new actor name")

    # PATCH actor -- Failure
    def test_404_update_actor(self):
        res = self.client().patch('actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")

    ''' MOVIES Tests '''

    # GET movie -- Success
    def test_movie(self):
        
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    # GET movie -- Failure
    def test_movie_not_found(self):
        
        res = self.client().get('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found.')

    # DELETE movie -- Success
    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE movie -- Failure
    def test_delete_not_found_movie(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found.')

    # POST movies -- Success
    def test_post_movie(self):
        res = self.client().post('/movies' , 
        json={
            "relase_date": "11-11-2021",
            "title": "new movie from test"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new movie'])

    # POST movie -- Failure
    def test_405_post_movie(self):
        res = self.client().post('/movies/1000' , json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed.")

    # PATCH movie -- Success
    def test_update_movie(self):
        res = self.client().patch('movies/7', json={'title': "new title form test"})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['title'], "new title form test")

    # PATCH movie -- Failure
    def test_404_update_movie(self):
        res = self.client().patch('movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")


if __name__ == "__main__":
    unittest.main()