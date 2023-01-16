#!/usr/bin/python3

"""This module handles utility functions for the API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """Returns status OK code"""
    return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_no_of_objects():
    """Retrieves the number of objects of each type from storage"""
    return jsonify({
        'Admins': storage.count('Admin'),
        'Customers': storage.count('Customer'),
        'Partners': storage.count('Partner'),
        'Routes': storage.count('Route'),
        'BookedTrips': storage.count('BookedTrip')
    })
