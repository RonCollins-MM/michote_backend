#!/usr/bin/python3

"""Contains customer class"""

from models.base_model import BaseModel

class Customer(BaseModel):
    """Use object definition"""

    first_name = ''

    last_name = ''

    age = 0

    gender = ''

    email = ''

    password = ''

    country = ''

    city = ''

    phone_number = ''

    trips_booked = 0
