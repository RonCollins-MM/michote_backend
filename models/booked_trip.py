#!/usr/bin/python3

"""Contains class definition for booked_trips objects"""

import models

from models.base_model import BaseModel, Base
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime

DATETIME_ISO = '%Y-%m-%dT%H:%M:%S.%f'

class BookedTrip(BaseModel, Base):
    """BookedTrip class implementation
    
    Attributes
    ----------
    route_id : str
        Unique ID given to each booked trip object.
    partner_id : str
        ID of partner who facilitated the trip
    customer_id : str
        ID of user who booked the trip
    no_of_seats_booked : int
        The number of seats booked for this trip
    total_amount : int
        The total amount of money paid for the trip


    Methods
    -------
    to_dict()
        Converts object from this class into a dict object with all attributes.
        Overrides the superclass' to_dict method.
    """
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
        """Creates a new BookedTrip object
        
        Uses super class constructor.
        """
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Converts object from BookedTrip class to dict

        Overrides BaseModels to_dict method because of additional DateTimes
        that need conversion to ISO format"""
        obj_as_dict = self.__dict__.copy()

        obj_as_dict.update({'__class__': f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()
        if '_sa_instance_state' in obj_as_dict:
            del obj_as_dict['_sa_instance_state']

        return obj_as_dict
