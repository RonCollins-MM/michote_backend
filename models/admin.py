#!/usr/bin/python3

"""Contains Admin class"""

from models.base_model import BaseModel

class Admin(BaseModel):
    """Admin Object definition"""

    username = ''

    email = ''

    password = ''

    phone_number = ''
