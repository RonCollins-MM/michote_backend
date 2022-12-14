#!/usr/bin/python3

"""Contains booked trips class"""

from models.base_model import BaseModel

class BookedTrips(BaseModel):
    """Implementation of booked trips class"""

    date_booked = ''

    company_id = ''

    customer_id = ''

    depature_location = ''

    destination = ''

    depature_time = ''

    arrival_time = ''

    no_of_seats_booked = 0

    price_per_ticket = 0

    total_amount = 0
