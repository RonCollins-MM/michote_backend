#!/usr/bin/python3

"""Contains booked trips class"""

from models.base_model import BaseModel

class BookedTrip(BaseModel):
    """Implementation of booked trips class"""

    date_booked = ''

    partner_id = ''

    customer_id = ''

    start_destination = ''

    end_destination = ''

    depature_time = ''

    arrival_time = ''

    no_of_seats_booked = 0

    price_per_ticket = 0

    currency = ''

    total_amount = 0
