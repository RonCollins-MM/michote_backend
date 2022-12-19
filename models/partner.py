#!/usr/bin/python3

"""Contains Partner class"""

from models.base_model import BaseModel

class Partner(BaseModel):
    """Implementation of booked trips class"""
    partner_name = ''

    phone_number = ''

    email = ''

    password = ''

    postal_address = ''

    country = ''
