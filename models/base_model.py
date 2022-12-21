#!/usr/bin/python3

"""
BaseClass Module - Contains implementation for the Base Class supercalss.
"""

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

    Defines all the attributes and methods common to all child classes.
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
        """Print this object"""

        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """Save the instance"""

        self.last_updated = datetime.datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert this object to dict"""

        obj_as_dict = self.__dict__.copy()

        obj_as_dict.update({'__class__' : f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()
        if '_sa_instance_state' in obj_as_dict:
            del obj_as_dict['_sa_instance_state']

        return obj_as_dict

    def delete(self):
        """Deletes the current instance from storage by calling
        storage.delete() method
        """
        models.storage.delete(self)
