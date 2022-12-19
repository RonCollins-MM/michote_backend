#!/usr/bin/python3

"""Contains Route class"""

from models.base_model import BaseModel

class Route(BaseModel):
    """Implementation of Route class"""

    timings = ''

    partner_id = ''

    start_destination = ''

    end_destination = ''

    period_begin = ''

    period_end = ''

    price_per_ticket = 0

    currency = ''

    slots_available = 0
