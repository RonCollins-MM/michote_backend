#!/usr/bin/python3

"""
BaseClass Module - Contains implementation for the Base Class supercalss.
"""

import uuid
import datetime
import models

class BaseModel():
    """BaseModel class implementation.

    Defines all the attributes and methods common to all child classes.
    """

    DATETIME_ISO = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *args, **kwargs):
        """BaseModel constructor."""

        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, value)
            if not hasattr(self, 'id'):
                self.id = str(uuid.uuid4())
            if not hasattr(self, 'created_at'):
                self.created_at = datetime.datetime.now()
                self.last_updated = self.created_at
            if type(self.created_at) is str:
                self.created_at = \
                datetime.datetime.strptime(kwargs['created_at'],
                                           BaseModel.DATETIME_ISO)
                self.last_updated = \
                datetime.datetime.strptime(kwargs['last_updated'],
                                           BaseModel.DATETIME_ISO)
            models.storage.new(self)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.last_updated = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Print this object"""

        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """Save the instance"""

        self.last_updated = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert this object to dict"""

        obj_as_dict = dict(self.__dict__)

        obj_as_dict.update({'__class__' : f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()

        return obj_as_dict
