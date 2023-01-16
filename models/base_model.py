#!/usr/bin/python3

"""Contains the BaseModel class definition."""

import uuid
import datetime
import models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv

if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel():
    """BaseModel class implementation.

    Defines attributes and methods common to all child classes. These will be
    inherited by all child classes.

    Attributes
    ----------
    id : str
        Unique ID assigned to each object created
    created_at : datetime obj
        Time stamp of when the object was created
    last_updated : datetime obj
        Time stamp of when the object was last updated
    DATETIME_ISO : str
        ISO standard date time format string. Used with the `datetime.strptime`
        method to convert datetime objects to string and vice versa.

    Methods
    -------
    __init__(*args, **kwargs)
        Creates a new object with attributes passed as a dictionary or as key-
        value pairs.
    __str__()
        Prints the string representation of objects of this class or child
        classes.
    save()
        Save an object of this class or child classes to storage
    to_dict()
        Converts the object from this class to dict objects with all attributes.
    delete()
        Deletes the object of this class or child classes from storage.
    """

    if models.storage_type == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    DATETIME_ISO = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *args, **kwargs):
        """BaseModel constructor."""

        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, value)
            if kwargs.get('id', None) is None:
                self.id = str(uuid.uuid4())
            if kwargs.get('created_at', None) is None:
                self.created_at = datetime.datetime.now()
                self.last_updated = self.created_at
            if type(self.created_at) is str:
                self.created_at = \
                datetime.datetime.strptime(kwargs['created_at'],
                                           BaseModel.DATETIME_ISO)
                self.last_updated = \
                datetime.datetime.strptime(kwargs['last_updated'],
                                           BaseModel.DATETIME_ISO)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.last_updated = self.created_at

    def __str__(self):
        """Prints an object created from this class, or from child classes as
        a string.
        """

        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """Save an object of this class or child classes to storage"""

        self.last_updated = datetime.datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert this object to dict object containing all attributes.
        
        All datetime objects are first converted to string format before being
        added to the dict.
        if `_sa_instance_state` attribute exists (a result of SQLALchemy), it is
        removed from the dict.
        """

        obj_as_dict = self.__dict__.copy()

        obj_as_dict.update({'__class__' : f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()
        if '_sa_instance_state' in obj_as_dict:
            del obj_as_dict['_sa_instance_state']

        return obj_as_dict

    def delete(self):
        """Deletes the object of this class or child classes from storage."""

        models.storage.delete(self)
