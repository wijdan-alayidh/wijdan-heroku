# Casting Agency 

## Full stack project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## The URL for app:

### https://wijdan-heroku.herokuapp.com/

## Auth0 and test endpoints:

This repo have a postman collection request to test all of the endpoints, this collection have the jwt token to check the endpoints


### Models:

1) Movies with attributes title and release date
2) Actors with attributes name, age and gender

### Endpoints:

1) GET /actors and /movies
2) DELETE /actors/ and /movies/
3) POST /actors and /movies and
4) PATCH /actors/ and /movies/

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

### Tests:
1) One test for success behavior of each endpoint
2) One test for error behavior of each endpoint
3) tests of RBAC for each role
