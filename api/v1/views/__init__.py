#!/usr/bin/python3
"""Blueprint creation and necessary imports"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.admins import *
from api.v1.views.booked_trips import *
from api.v1.views.customers import *
from api.v1.views.partners import *
from api.v1.views.routes import *
