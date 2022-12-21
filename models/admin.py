#!/usr/bin/python3

"""Contains Admin class"""

import models

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class Admin(BaseModel, Base):
    """Admin Object definition"""

    if models.storage_type == 'db':
        __tablename__ = 'admins'
        username = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
    else:
        username = ''
        email = ''
        password = ''
        phone_number = ''

    def __init__(self, *args, **kwargs):
        """Creates a new admin object"""
        super().__init__(*args,**kwargs)
