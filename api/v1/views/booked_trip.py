#!/usr/bin/python3

"""Api handler for BookedTrip objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.booked_trip import BookedTrip
from models.route import Route


bkd_trip_attributes = ['route_id', 'partner_id', 'customer_id', 'no_of_seats_booked', 'total_amount']

def desc_gen(missing_att_list):
    """Generates a description message with all attributes missing"""
    desc = 'Missing the following attributes: '
    for attr in missing_att_list:
        desc = desc + attr + ', '
    return desc[:-2]

@app_views.route('/bookings', methods=['GET'], strict_slashes=False)
def get_bookings():
    """Method called to get BookedTrip objects from storage.

    If a query string is passed with start_destination and end_destination, a
    matching object is returned from storage, if found.
    If no query string is passed, all BookedTrip objects are returned.
    If no matching object is found for query strin, empty dict is returned.
    """
    trips_list = []
    args = request.args
    if not args:
        trips_dict = storage.all(BookedTrip)
        for trip_obj in trips_dict.values():
            trips_list.append(trip_obj.to_dict())
        return jsonify(trips_list)

    if args('route_id'):
        route = args.get('route_id')
        trips_dict = storage.all(BookedTrip)
        for trip_obj in trips_dict.values():
            if trip_obj.route_id == route:
                trips_list.append(trip_obj.to_dict())
            
        return jsonify(trips_list)

    if args('customer_id'):
        customer = args.get('customer_id')
        trips_dict = storage.all(BookedTrip)
        for trip_obj in trips_dict.values():
            if trip_obj.customer_id == customer:
                trips_list.append(trip_obj.to_dict())
            
        return jsonify(trips_list)

@app_views.route('/bookings/<trip_id>', methods=['GET'], strict_slashes=False)
def get_one_trip(trip_id):
    """Method called to get one BookedTrip object based on its id"""
    trip = storage.get(BookedTrip, trip_id)

    if not trip:
        abort(404)
    return jsonify(trip.to_dict())

@app_views.route('/bookings/<trip_id>', methods=['DELETE'], strict_slashes=False)
def delete_trip(trip_id):
    """Deletes a specific trip record from storage"""
    trip = storage.get(BookedTrip, trip_id)

    if not trip:
        abort(404)
    storage.delete(trip)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('bookings', methods=['POST'], strict_slashes=False)
def add_new_trip():
    """Creates a new BookedTrip object"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    missing_atts = []
    for attribute in bkd_trip_attributes:
        if attribute not in request.get_json():
            missing_atts.append(attribute)
    if missing_atts:
        desc = desc_gen(missing_atts)
        abort(400, description=desc)

    info = request.get_json()
    trip_obj = BookedTrip(**info)
    trip_obj.save()

    return make_response(jsonify(trip_obj.to_dict()), 201)

@app_views.route('bookings/<trip_id>', methods=['PUT'], strict_slashes=False)
def update_trip(trip_id):
    """Updates BookedTrip information"""
    trip_obj = storage.get(BookedTrip, trip_id)

    if not trip_obj:
        abort(404)

    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')

    ignore_atts = ['id', 'created_at', 'last_updated']

    for key, value in info.items():
        if key not in ignore_atts:
            setattr(trip_obj, key, value)
    storage.save()
    return make_response(jsonify(trip_obj.to_dict()), 200)
