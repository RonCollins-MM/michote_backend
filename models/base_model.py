#!/usr/bin/python3

"""
BaseClass Module - Contains implementation for the Base Class supercalss.
"""

import uuid
import datetime

class BaseModel():
    """BaseModel class implementation.

    Defines all the attributes and methods common to all child classes.
    """

    def __init__(self, *args, **kwargs):
        """BaseModel constructor."""

        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'last_updated':
                    setattr(self, key, datetime.datetime.fromisoformat(value))
                    continue
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.last_updated = self.created_at

    def __str__(self):
        """Print this object"""

        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__})'

    def save(self):
        """Save the instance"""

        self.last_updated = datetime.datetime.now()

    def to_dict(self):
        """Convert this object to dict"""

        obj_as_dict = dict(self.__dict__)

        obj_as_dict.update({'__class__' : f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()

        return obj_as_dict
