#!/usr/bin/python3

"""Database storage engine for Michote."""

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
import urllib.parse

class DB_Storage:
    """Handles the database storage engine.
    
    Attributes
    ----------
    __classes : dict
        All valid classes in the Michote app. This private dict is used for
        validation to ensure only objects of valid classes are created.
    
    __engine : obj
        Holds the engine that interacts with the database.
        The database in use is MySQL.
    
    __session : obj
        Holds an instance of the current database session.
    
    MICHOTE_MYSQL_USER : str
    Username used to access the database

    MICHOTE_MYSQL_PWD : str
        Password used to access the database

    MICHOTE_MYSQL_HOST : str
        The IP where the server is hosted

    MICHOTE_MYSQL_DB : str
        The name of the database for the session

    MICHOTE_ENV : str
        The database environment for the session. Can be `dev` or `test`
    """

    __classes = {'Customer': Customer, 'Partner': Partner,
                 'BookedTrip': BookedTrip, 'Admin': Admin,
                 'Route': Route}

    __engine = None
    __session = None

    def __init__(self):
        """Initialises a database storage object.
        
        """
        MICHOTE_MYSQL_USER = getenv('MICHOTE_MYSQL_USER')
        MICHOTE_MYSQL_PWD = getenv('MICHOTE_MYSQL_PWD')
        MICHOTE_MYSQL_HOST = getenv('MICHOTE_MYSQL_HOST')
        MICHOTE_MYSQL_DB = getenv('MICHOTE_MYSQL_DB')
        MICHOTE_ENV = getenv('MICHOTE_ENV')
        
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MICHOTE_MYSQL_USER,
                                             urllib.parse.quote_plus(MICHOTE_MYSQL_PWD),
                                             MICHOTE_MYSQL_HOST,
                                             MICHOTE_MYSQL_DB))
        if MICHOTE_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all the objects stored in the database.

        If class name is specified, only objects from that class are returned.
        Otherwise, all objects in the database are returned
        
        Parameters
        ----------
        cls : str, optional
            The class whose objects are to be returned
        """
        objs_dict = {}
        for clss in DB_Storage.__classes:
            if cls is None or cls is DB_Storage.__classes[clss] or cls is clss:
                objs = self.__session.query(DB_Storage.__classes[clss]).all()
                for obj in objs:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    objs_dict[key] = obj
        return objs_dict

    def new(self, obj):
        """Adds a new object to the current database session
        
        Parameters
        ----------
        obj : str
            The object to be added to storage.
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes made in the current session to the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the passed object from the database.

        If no object is passed, does nothing
        
        Parameters
        ----------
        obj : object, optional
            The object to be deleted from storage
        """
        if obj is None:
            return
        self.__session.delete(obj)

    def reload(self):
        """Reloads all objects from the database to the current session"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Closes the current database session"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieves an object from storage based on its class name and ID.
        
        Parameters
        ----------
        cls : str
            The class of the object
        id : str
            The ID of the object

        Returns
        -------
        obj
            The object that has been retrieved, if found.
        """
        if cls not in DB_Storage.__classes.values():
            return None

        objs_dict = models.storage.all(cls)
        for obj in objs_dict.values():
            if (obj.id == id):
                return obj

        return None

    def count(self, cls=None):
        """Counts the number of objects of a given class in storage.

        If no class name is given, all objects in storage are counted.
        
        Parameters
        ----------
        cls : str, optional
            The class name whose objects are to be counted.

        Returns
        -------
        int
            The total number of objects counted
        """
        return len(self.all(cls))
