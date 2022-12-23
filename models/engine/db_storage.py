#!/usr/bin/python3

"""This module handles the database storage engine"""

import models

from os import getenv
from sqlalchemy import create_engine
from models.customer import Customer
from models.partner import Partner
from models.route import Route
from models.admin import Admin
from models.booked_trip import BookedTrip
from models.base_model import Base
from sqlalchemy.orm import scoped_session, sessionmaker

class DB_Storage:
    """Defines the database storage engine attributes"""

    __classes = {'Customer': Customer, 'Partner': Partner,
                 'BookedTrip': BookedTrip, 'Admin': Admin,
                 'Route': Route}

    __engine = None
    __session = None

    def __init__(self):
        """Initialises a database storage object"""
        MICHOTE_MYSQL_USER = getenv('MICHOTE_MYSQL_USER')
        MICHOTE_MYSQL_PWD = getenv('MICHOTE_MYSQL_PWD')
        MICHOTE_MYSQL_HOST = getenv('MICHOTE_MYSQL_HOST')
        MICHOTE_MYSQL_DB = getenv('MICHOTE_MYSQL_DB')
        MICHOTE_ENV = getenv('MICHOTE_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MICHOTE_MYSQL_USER,
                                             MICHOTE_MYSQL_PWD,
                                             MICHOTE_MYSQL_HOST,
                                             MICHOTE_MYSQL_DB))
        if MICHOTE_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all the objects stored in the database.

        If class name is specified, only objects from that class are returned.
        Otherwise, all objects in the database are returned"""
        objs_dict = {}
        for clss in DB_Storage.__classes:
            if cls is None or cls is DB_Storage.__classes[clss] or cls is clss:
                objs = self.__session.query(DB_Storage.__classes[clss]).all()
                for obj in objs:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    objs_dict[key] = obj
        return objs_dict

    def new(self, obj):
        """Adds a new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes made in the current session to the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the passed object from the database

        If no object is passed, does nothing"""
        if obj is None:
            return
        self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Closes the current database session"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieves an object from storage"""
        if cls not in DB_Storage.__classes.values():
            return None

        objs_dict = models.storage.all(cls)
        for obj in objs_dict.values():
            if (obj.id == id):
                return obj

        return None

    def count(self, cls=None):
        """Counts the number of objects of a given class in storage"""
        return len(self.all(cls))
