#!/usr/bin/python3

"""Api handler for Partner objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.partner import Partner

partner_attributes = ['partner_name', 'postal_address', 'email',
                       'password', 'country', 'phone_number']

def desc_gen(missing_att_list):
    """Generates a description message with all attributes missing"""
    desc = 'Missing the following attributes: '
    for attr in missing_att_list:
        desc = desc + attr + ', '
    return desc[:-2]

@app_views.route('/partners', methods=['GET'], strict_slashes=False)
def get_all_partners():
    """Method called to get all Partner objects from storage"""
    partner_list = []

    partner_dict = storage.all(Partner)
    if not partner_dict:
        abort(404)
    for partner_obj in partner_dict.values():
        partner_list.append(partner_obj.to_dict())

    return jsonify(partner_list)

@app_views.route('/partners/<partner_id>', methods=['GET'], strict_slashes=False)
def get_one_partner(partner_id):
    """Method called to get one partner object based on its id"""
    partner = storage.get(Partner, partner_id)

    if not partner:
        abort(404)
    return jsonify(partner.to_dict())

@app_views.route('/partners/<partner_id>', methods=['DELETE'], strict_slashes=False)
def delete_partner(partner_id):
    """Deletes a specific partner object from storage"""
    partner = storage.get(Partner, partner_id)

    if not partner:
        abort(404)
    storage.delete(partner)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('partners/signup', methods=['POST'], strict_slashes=False)
def create_partner():
    """Creates a new Partner object"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    missing_atts = []
    for attribute in partner_attributes:
        if attribute not in request.get_json():
            missing_atts.append(attribute)
    if missing_atts:
        desc = desc_gen(missing_atts)
        abort(400, description=desc)

    partner_dict = storage.all(Partner)
    for partner_obj in partner_dict.values():
        if partner_obj.email == request.get_json()['email']:
            abort(409, description='Partner with that email already exists')

    info = request.get_json()
    partner_obj = Partner(**info)
    partner_obj.save()

    return make_response(jsonify(partner_obj.to_dict()), 201)

@app_views.route('partners/login', methods=['POST'], strict_slashes=False)
def auth_partner():
    """Checks if Partner with given credentials exists in storage.

    If found, returns 200 OK response. Otherwise, returns 404 not found
    """
    if 'email' not in request.get_json():
        desc = desc_gen(['email'])
        abort(400, description=desc)
    if 'password' not in request.get_json():
        desc = desc_gen(['password'])
        abort(400, description=desc)

    partner_dict = storage.all(Partner)
    for partner_obj in partner_dict.values():
        if partner_obj.email == request.get_json()['email'] and \
           partner_obj.password == request.get_json()['password']:
            return make_response(jsonify({'auth_status':'SUCCESS'}), 200)
    return make_response(jsonify({'auth_status':'FAIL'}), 404)

@app_views.route('partners/<partner_id>', methods=['PUT'], strict_slashes=False)
def update_partner(partner_id):
    """Updates partner information"""
    partner_obj = storage.get(Partner, partner_id)

    if not partner_obj:
        abort(404)

    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')

    ignore_atts = ['id', 'created_at', 'last_updated']

    for key, value in info.items():
        if key not in ignore_atts:
            setattr(partner_obj, key, value)
    storage.save()
    return make_response(jsonify(partner_obj.to_dict()), 200)
