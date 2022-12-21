#!/usr/bin/python3

"""Contains customer class"""

import models

from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer

class Customer(BaseModel, Base):
    """Use object definition"""
    if models.storage_type == 'db':
        __tablename__='customers'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        age = Column(Integer, nullable=False)
        gender = Column(String(128), nullable=True, default='prefer not to say')
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        country = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
        trips_booked = Column(Integer, nullable=True, default=0)
    else:
        first_name = ''
        last_name = ''
        age = 0
        gender = ''
        email = ''
        password = ''
        country = ''
        phone_number = ''
        trips_booked = 0

    def __init__(self, *args, **kwargs):
        """Creates a new Customer object"""
        super().__init__(*args, **kwargs)
