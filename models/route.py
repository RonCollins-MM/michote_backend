#!/usr/bin/python3

"""Contains Route class"""

import models

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from os import getenv

class Route(BaseModel, Base):
    """Implementation of Route class"""
    if models.storage_type == 'db':
        __tablename__ = 'routes'
        partner_id = Column(String(60), ForeignKey('partners.id'),
                            nullable=True)
        start_destination = Column(String(60), nullable=False)
        end_destination = Column(String(60), nullable=False)
        period_begin = Column(DateTime, nullable=True)
        period_end = Column(DateTime, nullable=True)
        price_per_ticket = Column(Integer, nullable=True)
        currency = Column(String(128), nullable=True)
        slots_available = Column(Integer, nullable=True)
    else:
        partner_id = ''
        start_destination = ''
        end_destination = ''
        period_begin = ''
        period_end = ''
        price_per_ticket = 0
        currency = ''
        slots_available = 0

    def __init__(self, *args, **kwargs):
        """Creates new Route object"""
        super().__init__(*args, **kwargs)
