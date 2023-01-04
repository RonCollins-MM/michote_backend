#!/usr/bin/python3

"""Contains booked trips class"""

import models

from models.base_model import BaseModel, Base
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime

DATETIME_ISO = '%Y-%m-%dT%H:%M:%S.%f'

class BookedTrip(BaseModel, Base):
    """Implementation of booked trips class"""
    if models.storage_type == 'db':
        __tablename__ = 'booked_trips'
        route_id = Column(String(60), nullable=False)
        partner_id = Column(String(60), nullable=False)
        customer_id = Column(String(60), nullable=False)
        no_of_seats_booked = Column(Integer, nullable=False)
        total_amount = Column(Integer, nullable=False, default=0)
    else:
        route_id = ''
        partner_id = ''
        customer_id = ''
        no_of_seats_booked = 0
        total_amount = 0

    def __init__(self, *args, **kwargs):
        """Creates a new BookedTrip object"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Converts object from BookedTrip class to dict

        This is the only class that overrides BaseModels to_dict method because
        of additional DateTimes that need conversion to ISO format"""
        obj_as_dict = self.__dict__.copy()

        obj_as_dict.update({'__class__': f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()
        if '_sa_instance_state' in obj_as_dict:
            del obj_as_dict['_sa_instance_state']

        return obj_as_dict
