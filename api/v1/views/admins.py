#!/usr/bin/python3

"""Api handler for admin objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.admin import Admin

admin_attributes = ['username', 'password', 'email', 'phone_number']

def desc_gen(missing_att_list):
    """Generates a description message with all attributes missing"""
    desc = 'Missing the following attributes: '
    for attr in missing_att_list:
        desc = desc + attr + ', '
    return desc[:-2]

@app_views.route('/admins', methods=['GET'], strict_slashes=False)
def get_all_admins():
    """Method called to get all Admin objects from storage"""
    admins_list = []

    admins_dict = storage.all(Admin)
    if not admins_dict:
        abort(404)
    for admin_obj in admins_dict.values():
        admins_list.append(admin_obj.to_dict())

    return jsonify(admins_list)

@app_views.route('/admins/<admin_id>', methods=['GET'], strict_slashes=False)
def get_one_admin(admin_id):
    """Method called to get one Admin object based on its id"""
    admin = storage.get(Admin, admin_id)

    if not admin:
        abort(404)
    return jsonify(admin.to_dict())

@app_views.route('/admins/<admin_id>', methods=['DELETE'], strict_slashes=False)
def delete_admin(admin_id):
    """Deletes a specific admin record from storage"""
    admin = storage.get(Admin, admin_id)

    if not admin:
        abort(404)
    storage.delete(admin)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('admins/signup', methods=['POST'], strict_slashes=False)
def create_admin():
    """Creates a new admin object"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    missing_atts = []
    for attribute in admin_attributes:
        if attribute not in request.get_json():
            missing_atts.append(attribute)
    if missing_atts:
        desc = desc_gen(missing_atts)
        abort(400, description=desc)

    admin_dict = storage.all(Admin)
    for admin_obj in admin_dict.values():
        if admin_obj.email == request.get_json()['email']:
            abort(409, description='User with that email already exists')

    info = request.get_json()
    admin_obj = Admin(**info)
    admin_obj.save()

    return make_response(jsonify(admin_obj.to_dict()), 201)

@app_views.route('admins/login', methods=['POST'], strict_slashes=False)
def auth_admin():
    """Checks if admin with given credentials exists in storage.

    If found, returns 200 OK response. Otherwise, returns 404 not found
    """
    if 'email' not in request.get_json():
        desc = desc_gen(['email'])
        abort(400, description=desc)
    if 'password' not in request.get_json():
        desc = desc_gen(['password'])
        abort(400, description=desc)

    admins_dict = storage.all(Admin)
    for admin_obj in admins_dict.values():
        if admin_obj.email == request.get_json()['email'] and \
           admin_obj.password == request.get_json()['password']:
            return make_response(jsonify({'auth_status':'SUCCESS'}), 200)
    return make_response(jsonify({'auth_status':'FAIL'}), 404)
