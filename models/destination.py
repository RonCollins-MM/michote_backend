#!/usr/bin/python3

"""Contains Destination class"""

from models.base_model import BaseModel

class Prices(BaseModel):
    """Implementation of destination class"""

    latitude = 0.0

    longitude = 0.0

    country = ''

    name = ''

    number_of_bookings = 0
