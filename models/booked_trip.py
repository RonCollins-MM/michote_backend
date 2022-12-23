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
        date_booked = Column(DateTime, nullable=False,
                             default=datetime.utcnow())
        partner_id = Column(String(60), nullable=False)
        customer_id = Column(String(60), nullable=False)
        start_destination = Column(String(128), nullable=False)
        end_destination = Column(String(128), nullable=False)
        departure_time = Column(DateTime, nullable=False,
                               default=datetime.utcnow())
        arrival_time = Column(DateTime, nullable=False,
                              default=datetime.utcnow())
        no_of_seats_booked = Column(Integer, nullable=False)
        price_per_ticket = Column(Integer, nullable=False)
        currency = Column(String(128), nullable=False)
        total_amount = Column(Integer, nullable=False, default=0)
    else:
        date_booked = ''
        partner_id = ''
        customer_id = ''
        start_destination = ''
        end_destination = ''
        departure_time = ''
        arrival_time = ''
        no_of_seats_booked = 0
        price_per_ticket = 0
        currency = ''
        total_amount = 0

    def __init__(self, *args, **kwargs):
        """Creates a new BookedTrip object"""
        super().__init__(*args, **kwargs)

        if type(self.date_booked) is str:
            self.date_booked = datetime.strptime(self.date_booked,
                                                 DATETIME_ISO)
        if type(self.departure_time) is str:
            self.departure_time = datetime.strptime(self.departure_time,
                                                   DATETIME_ISO)
        if type(self.arrival_time) is str:
            self.arrival_time = datetime.strptime(self.arrival_time,
                                                  DATETIME_ISO)

    def to_dict(self):
        """Converts object from BookedTrip class to dict

        This is the only class that overrides BaseModels to_dict method because
        of additional DateTimes that need conversion to ISO format"""
        obj_as_dict = self.__dict__.copy()

        obj_as_dict.update({'__class__': f'{self.__class__.__name__}'})
        obj_as_dict['created_at'] = self.created_at.isoformat()
        obj_as_dict['last_updated'] = self.last_updated.isoformat()
        obj_as_dict['departure_time'] = self.departure_time.isoformat()
        obj_as_dict['arrival_time'] = self.arrival_time.isoformat()
        obj_as_dict['date_booked'] = self.date_booked.isoformat()
        if '_sa_instance_state' in obj_as_dict:
            del obj_as_dict['_sa_instance_state']

        return obj_as_dict
