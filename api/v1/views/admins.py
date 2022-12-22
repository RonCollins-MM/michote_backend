#!/usr/bin/python3

"""Api handler for admin objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.admin import Admin

admin_attributes = ['username', 'password', 'email', 'phone_number']

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
    for attribute in admin_attributes:
        if attribute not in request.get_json():
            abort(400, description=f'Missing {attribute}')

    info = request.get_json()
    admin_obj = Admin(**info)
    admin_obj.save()

    return make_response(jsonify(admin_obj.to_dict()), 201)

