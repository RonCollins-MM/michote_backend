#!/usr/bin/python3

"""Api handler for Route objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.route import Route

route_attributes = ['partner_id', 'start_destination', 'end_destination', 'period_begin',
                    'period_end', 'price_per_ticket', 'currency',
                    'slots_available']

def desc_gen(missing_att_list):
    """Generates a description message with all attributes missing"""
    desc = 'Missing the following attributes: '
    for attr in missing_att_list:
        desc = desc + attr + ', '
    return desc[:-2]

@app_views.route('/routes', methods=['GET'], strict_slashes=False)
def get_matching_routes():
    """Method called to get all Routes objects from storage.

    If a query strin is passed with start_destination and end_destination, a
    matching object is returned from storage, if found.
    If no query string is passed, all route objects are returned.
    """
    routes_list = []
    args = request.args
    if not args:
        routes_dict = storage.all(Route)
        for route_obj in routes_dict.values():
            routes_list.append(route_obj.to_dict())
        return jsonify(routes_list)

    if args.get('partner_id'):
        partner = args.get('partner_id')
        routes_dict = storage.all(Route)
        for route_obj in routes_dict.values():
            if route_obj.partner_id == partner:
                routes_list.append(route_obj.to_dict())

    start_dest = args.get('start_destination')
    end_dest = args.get('end_destination')
    if not start_dest:
        abort(400, description='Missing start_destination in query string')
    if not end_dest:
        abort(400, description='Missing end_destination in query string')

    routes_dict = storage.all(Route)
    for route_obj in routes_dict.values():
        if route_obj.start_destination == start_dest and \
           route_obj.end_destination == end_dest:
            routes_list.append(route_obj.to_dict())

    return jsonify(routes_list)

@app_views.route('/routes/<route_id>', methods=['GET'], strict_slashes=False)
def get_one_route(route_id):
    """Method called to get one Route object based on its id"""
    route = storage.get(Route, route_id)

    if not route:
        abort(404)
    return jsonify(route.to_dict())

@app_views.route('/routes/<route_id>', methods=['DELETE'], strict_slashes=False)
def delete_route(route_id):
    """Deletes a specific route record from storage"""
    route = storage.get(Route, route_id)

    if not route:
        abort(404)
    storage.delete(route)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('routes', methods=['POST'], strict_slashes=False)
def create_route():
    """Creates a new route object"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    missing_atts = []
    for attribute in route_attributes:
        if attribute not in request.get_json():
            missing_atts.append(attribute)
    if missing_atts:
        desc = desc_gen(missing_atts)
        abort(400, description=desc)

    route_dict = storage.all(Route)
    rpartner_id = request.get_json()['partner_id']
    rstart_destination = request.get_json()['start_destination']
    rend_destination = request.get_json()['end_destination']
    for route_obj in route_dict.values():
        if route_obj.partner_id == rpartner_id and \
        route_obj.start_destination == rstart_destination and \
           route_obj.end_destination == rend_destination:
            abort(409, description='That route already exists !')

    info = request.get_json()
    route_obj = Route(**info)
    route_obj.save()

    return make_response(jsonify(route_obj.to_dict()), 201)

@app_views.route('routes/<route_id>', methods=['PUT'], strict_slashes=False)
def update_route(route_id):
    """Updates route information"""
    route_obj = storage.get(Route, route_id)

    if not route_obj:
        abort(404)

    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')

    ignore_atts = ['id', 'created_at', 'last_updated', 'partner_id']

    for key, value in info.items():
        if key not in ignore_atts:
            setattr(route_obj, key, value)
    storage.save()
    return make_response(jsonify(route_obj.to_dict()), 200)
