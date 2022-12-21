#!/usr/bin/python3

"""Contains Partner class"""

import models

from models.base_model import BaseModel, Base
from os import getenv
from models.route import Route
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Partner(BaseModel, Base):
    """Implementation of booked trips class"""

    if models.storage_type == 'db':
        __tablename__ = 'partners'
        partner_name = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        postal_address = Column(String(128), nullable=True)
        country = Column(String(128), nullable=False)
        routes = relationship('Route', backref='partner')
    else:
        partner_name = ''
        phone_number = ''
        email = ''
        password = ''
        postal_address = ''
        country = ''

    def __init__(self, *args, **kwargs):
        """Constructor for Partner class"""
        super().__init__(*args, **kwargs)

    if models.storage_type != 'db':
        @property
        def routes(self):
            """Getter for all the routes under the current partner"""
            routes_list = []
            all_routes = models.storage.all(Route)
            for route in all_routes.values():
                if route.partner_id == self.id:
                    routes_list.append(route)
            return routes_list
