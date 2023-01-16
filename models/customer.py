#!/usr/bin/python3

"""Contains User class implementation"""

import models

from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer

class Customer(BaseModel, Base):
    """User object definition.

    If storage type is database, all attributes are mapped to MySQL table
    columns.

    
    Attributes
    ----------
    first_name : str
        First name of user
    last_name : str
        Last name of user
    email : str
        Email of user
    password : str
        Password of user
    country : str
        Country where the user resides
    phone_number : str
        Phone number of user
    trips_booked : int
        Total number of trips booked by user.

    """
    if models.storage_type == 'db':
        __tablename__ = 'customers'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        country = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
        trips_booked = Column(Integer, nullable=True, default=0)
    else:
        first_name = ''
        last_name = ''
        email = ''
        password = ''
        country = ''
        phone_number = ''
        trips_booked = 0

    def __init__(self, *args, **kwargs):
        """Creates a new Customer object"""
        super().__init__(*args, **kwargs)
