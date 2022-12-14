#!/usr/bin/python3

"""Contains prices class"""

from models.base_model import BaseModel

class Prices(BaseModel):
    """Implementation of Prices class"""

    timings = ''

    company_id = ''

    start_destination_id = ''

    end_destination_id = ''

    period_begin = ''

    period_end = ''

    price_per_ticket = 0
