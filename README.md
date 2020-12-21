# Casting Agency Full stack project

## About

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Motivation

Over the past four months, I have learned a lot of things in this field through this nanodegree.
Many of them I thought were difficult or might not be possible for me, at least for now.
It was a period in which I challenged myself first and those fears and thoughts second, and this project is like proof to me that I can.
This project is a summary of what I learned during this beautiful and enjoyable journey for me and I hope it will be useful to you.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) or [flask docs](https://flask.palletsprojects.com/en/1.1.x/installation/).

In general you can create the Virtual Enviornment by using this command inside the parent project directory `/wijdan-heroku` :

```bash
$ python3 -m venv venv
```

to activate the Virtual Enviornment use this command in terminal:

```bash
$ . venv/bin/activate
```

to deactivate the Virtual Enviornment use this command in terminal:

```bash
$ deactivate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/wijdan-heroku` directory and running:

```bash
$ pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight postgres database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests. 

## Database Setup
With Postgres running, restore a database using the movies.psql file provided. From the `wijdan-heroku` folder in terminal run:

```bash
psql movies < movies.psql
```

## Running the server

From within the `wijdan-heroku` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run --reload
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` directory. 


### Models:

1) Movies with attributes title and release date
2) Actors with attributes name, age and gender

### Endpoints:

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user.

1) GET /actors and /movies
2) DELETE /actors/ and /movies/
3) POST /actors and /movies and
4) PATCH /actors/ and /movies/

#### GET '/actors'
- Fetches all available data about all actors in the database
- Request Arguments: jwt
- Returns: An Json object contain actors name, age, gender and id.

Sample of response output:

{
    "actors": [
        {
            "age": "22",
            "gender": "male",
            "id": 4,
            "name": "test"
        },
        {
            "age": "22",
            "gender": "male",
            "id": 5,
            "name": "test"
        },
        {
            "age": "22",
            "gender": "male",
            "id": 6,
            "name": "test"
        }
}

#### GET '/actors/{actor_id}'
- Fetches available data about specific actor in the database based on the actor id that is passed through the request.
- Request Arguments: jwt, actor_id.
- Returns: An Json object contain actor name, age, gender and id.

Sample of response output:

{
    "Actor": {
        "age": "22",
        "gender": "male",
        "id": 4,
        "name": "test"
    },
    "success": true
}


#### GET '/movies'
- Fetches all available data about all movies in the database.
- Request Arguments: jwt
- Returns: An Json object contain movies relase date, title and id.

Sample of response output:

{
    "movies": [
        {
            "id": 2,
            "relase_date": "11-11-2021",
            "title": "new movie"
        },
        {
            "id": 3,
            "relase_date": "11-11-2021",
            "title": "new movie"
        },
        {
            "id": 4,
            "relase_date": "11-11-2021",
            "title": "new movie"
        }
}

#### GET '/movies/{actor_id}'
- Fetches available data about specific movie in the database based on the movie id that is passed through the request.
- Request Arguments: jwt, movie_id.
- Returns: An Json object contain movies relase date, title and id.

Sample of response output:

{
    "movie": {
        "id": 1,
        "relase_date": "12-12-2012",
        "title": "update movie title"
    },
    "success": true
}


#### DELETE '/actors/{actor_id}'
- Delete the data about specifiec actor.
- Request Arguments: jwt, actor_id.
- Returns: An Json object contain name of the deleted actor.

Sample of response output:

{
    "Deleted Actor": "actor name",
    "success": true
}


#### DELETE '/movies/{movie_id}'
- Delete the data about specifiec movie.
- Request Arguments: jwt, movie_id.
- Returns: An Json object contain title of the deleted movie.

Sample of response output:

{
    "Deleted Movie": "new movie",
    "success": true
}


#### POST '/actors'
- Post new actor into the database.
- Request Arguments: jwt, also in the request body need to add JSON object include all data about new actor thats contain actor name, age and gender the request body should formed like this:

{
    "name": "new actor name",
    "age": 27,
    "gender":"male"
}

- Returns: An Json object contain new posted contain new actor name, age, gender and id.

Sample of response output:

{
    "new actor": {
        "age": "27",
        "gender": "male",
        "id": 25,
        "name": " new actor name"
    },
    "success": true
}

#### POST '/movies'
- Post new movie into the database.
- Request Arguments: jwt, also in the request body need to add JSON object include all data about new movie thats contain movie relase date and its title the request body should formed like this:

{
    "relase_date": "11-11-2021",
    "title": "new movie title"
}

- Returns: An Json object contain new posted movie relase date, title and id.

Sample of response output:

{
    "new movie": {
        "id": 27,
        "relase_date": "11-11-2021",
        "title": "new movie title"
    },
    "success": true
}


#### PATCH '/actors/{actor_id}'
- Update actor data based on the actor id.
- Request Arguments: jwt, actor_id also in the request body need to add JSON object include data that needed to update like actor name, age, or gender the request body should formed like this based on the data you want to update :

Update actor name:

{
    "name": "update actor name"
}

Update actor age:

{
    "age": "22"
}

Update actor gender:

{
    "gender": "female"
}

- Returns: An Json object contain updated actor age, gender, name and id.

Sample of response output:

{
    "Actor Information": {
        "age": "22",
        "gender": "female",
        "id": 1,
        "name": "update actor name"
    },
    "success": true
}



#### PATCH '/movies/{movie_id}'
- Update movie data based on the movie id.
- Request Arguments: jwt, movie_id also in the request body need to add JSON object include data that needed to update like movie title or relase date the request body should formed like this based on the data you want to update :

Update movie title:

{
    "title": "new movie title"
}

Update movie relase date:

{
    "relase_date": "11-11-2021"
}

- Returns: An Json object contain updated movie relase date, title and id.

Sample of response output:

{
    "Movie Information": {
        "id": 1,
        "relase_date": "12-12-2012",
        "title": "update movie title"
    },
    "success": true
}


### Roles:

1) Casting Assistant
  - Can view actors and movies

2) Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
  
3) Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

## THIRD-PARTY AUTHENTICATION
#### auth/auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:

- The Auth0 Domain Name
- Auth ALGORITHMS
- API AUDIENCE 
- The JWT code

The JWT token contains the permissions for the 'Producer' roles.

## Tests:

There are 16 unittests in test_app.py. To run this file use:

```bash
$ dropdb movies
$ createdb movies
$ psql movies < movies.psql
$ python3 test_app.py
```

The tests include:

1) One test for success behavior of each endpoint
2) One test for error behavior of each endpoint
3) tests of RBAC for each role

where all endpoints are tested with and without the correct authorization.
Further, the file 'Project tests.postman_collection.json' contains postman tests containing tokens for specific roles.


To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> wijdan-heroku/Project tests.postman_collection.json
3. Click on the runner, select the collection and run all the tests.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
### https://wijdan-heroku.herokuapp.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.
This app have a postman collection of all possible requests for this app you can use it for test endpoints.
