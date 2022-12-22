#!/usr/bin/python3

"""This module handles utility functions for the API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """Returns status OK code"""
    return jsonify({'status': 'OK'})
