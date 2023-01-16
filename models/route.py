#!/usr/bin/python3

"""Contains implementation of route class"""

import models

from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from os import getenv

DATETIME_ISO = '%Y-%m-%dT%H:%M'

class Route(BaseModel, Base):
    """Route object definition.
    
    Attributes
    ----------
    partner_id : str
        ID of partner company who created this route.
    start_destination : str
        The start destination of the route
    end_destination : str
         The end destination of the route
    period_begin : datetime
        The beginning of the period during which this route is valid for the
        respective partner comnpany
    period_end : datetime
        The end of the period during which this route is valid for the
        respective partner comnpany
    price_per_ticket : int
        The price for each ticket for this route
    currency : str
        The currency for the price per ticket
    slots_available : int
        The slots available for this route
    """
    if models.storage_type == 'db':
        __tablename__ = 'routes'
        partner_id = Column(String(60), ForeignKey('partners.id'),
                            nullable=True)
        start_destination = Column(String(60), nullable=False)
        end_destination = Column(String(60), nullable=False)
        period_begin = Column(DateTime, nullable=True)
        period_end = Column(DateTime, nullable=True)
        price_per_ticket = Column(Integer, nullable=True)
        currency = Column(String(128), nullable=True)
        slots_available = Column(Integer, nullable=True)
    else:
        partner_id = ''
        start_destination = ''
        end_destination = ''
        period_begin = ''
        period_end = ''
        price_per_ticket = 0
        currency = ''
        slots_available = 0

    def __init__(self, *args, **kwargs):
        """Creates new Route object.
        
        Parameters
        ----------
        *args : key/value pairs, optional
            Attributes passed as key value pairs passed
        **kwargs : dict, optional
            Dict object that contains all attributes for creating new object
        """
        super().__init__(*args, **kwargs)

        if type(self.period_begin) is str:
            self.period_begin = datetime.strptime(self.period_begin,
                                                  DATETIME_ISO)
        if type(self.period_end) is str:
            self.period_end = datetime.strptime(self.period_end, DATETIME_ISO)
