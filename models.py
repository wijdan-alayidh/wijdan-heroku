import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime, Date
from flask_sqlalchemy import SQLAlchemy
import json
import enum
from datetime import datetime

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup database :
    binds a flask application and SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    # db.drop_all()
    db.create_all()


'''
Association table to make the many to many,
relationship between Movies & Actors class
'''

# association = db.Table('association',
#                         db.Column('movie_id', db.Integer,
#                         db.ForeignKey('movies.id'), primary_key=True),
#                         db.Column('actor_id', db.Integer,
#                         db.ForeignKey('actors.id'), primary_key=True)
# )


'''
Movies Model
'''


class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    relase_date = Column(Date, nullable=False)
    # actors = db.relationship('Actors',
    #                         secondary = association,
    #                         backref = 'actors')

    def __init__(self, title, relase_date):
        self.title = title
        self.relase_date = relase_date
        # self.actors = actors

    # This function for define the the representation format from this Model
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'relase_date': self.relase_date.strftime('%m-%d-%Y')

        }

    # This function to insert new record into the table
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # This function to update or midify inserted record from the table
    def update(self):
        db.session.commit()

    # This function to delete recored from the table
    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
This class to use it in gender column to selecte between available choices
    -- Male
    -- Female
    -- Undefined
'''


class Gender_choices(enum.Enum):
    male = 'Male'
    female = 'Female'
    not_defined = 'Undefined'


'''
Actors Model
'''


class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(String)
    # Here use the Enum and Gender_choices class to make the choices available
    # to select between it
    gender = Column(String, db.Enum(Gender_choices),
                    default=Gender_choices.not_defined,
                    nullable=False)
    # movies = db.relationship('Movies',
    #                           secondary = association,
    #                           backref = 'movies')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        # self.movies = movies

    # This function for define the the representation format from this Model
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    # This function to insert new record into the table
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # This function to update or midify inserted record from the table
    def update(self):
        db.session.commit()

    # This function to delete recored from the table
    def delete(self):
        db.session.delete(self)
        db.session.commit()
