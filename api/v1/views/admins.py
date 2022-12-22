#!/usr/bin/python3

"""Api handler for admin objects"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.admin import Admin


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
