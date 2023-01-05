#!/usr/bin/python3

"""Api handler for Customer objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.customer import Customer

customer_attributes = ['first_name', 'last_name', 'email',
                       'password', 'country', 'phone_number']

def desc_gen(missing_att_list):
    """Generates a description message with all attributes missing"""
    desc = 'Missing the following attributes: '
    for attr in missing_att_list:
        desc = desc + attr + ', '
    return desc[:-2]

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Method called to get all User objects from storage"""
    customer_list = []

    customer_dict = storage.all(Customer)
    for customer_obj in customer_dict.values():
        customer_list.append(customer_obj.to_dict())

    return jsonify(customer_list)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_one_user(user_id):
    """Method called to get one User object based on its id"""
    customer = storage.get(Customer, user_id)

    if not customer:
        abort(404)
    return jsonify(customer.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific user from storage"""
    customer = storage.get(Customer, user_id)

    if not customer:
        abort(404)
    storage.delete(customer)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    missing_atts = []
    for attribute in customer_attributes:
        if attribute not in request.get_json():
            missing_atts.append(attribute)
    if missing_atts:
        desc = desc_gen(missing_atts)
        abort(400, description=desc)

    customer_dict = storage.all(Customer)
    for customer_obj in customer_dict.values():
        if customer_obj.email == request.get_json()['email']:
            abort(409, description='User with that email already exists')

    info = request.get_json()
    customer_obj = Customer(**info)
    customer_obj.save()

    return make_response(jsonify(customer_obj.to_dict()), 201)

@app_views.route('users/login', methods=['POST'], strict_slashes=False)
def auth_user():
    """Checks if Customer with given credentials exists in storage.

    If found, returns 200 OK response. Otherwise, returns 404 not found
    """
    if 'email' not in request.get_json():
        desc = desc_gen(['email'])
        abort(400, description=desc)
    if 'password' not in request.get_json():
        desc = desc_gen(['password'])
        abort(400, description=desc)

    customer_dict = storage.all(Customer)
    for customer_obj in customer_dict.values():
        if customer_obj.email == request.get_json()['email'] and \
           customer_obj.password == request.get_json()['password']:
            return make_response(jsonify({'auth_status':'SUCCESS', 'user_id': customer_obj.id}), 200)
    return make_response(jsonify({'auth_status':'FAIL'}), 404)

@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates customer information"""
    customer_obj = storage.get(Customer, user_id)

    if not customer_obj:
        abort(404)

    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')

    ignore_atts = ['id', 'created_at', 'last_updated']

    for key, value in info.items():
        if key not in ignore_atts:
            setattr(customer_obj, key, value)
    storage.save()
    return make_response(jsonify(customer_obj.to_dict()), 200)
