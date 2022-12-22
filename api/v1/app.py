#!/usr/bin/python3

"""This module handles environment setup for michote API"""

from flask import Flask, make_response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

host = getenv('MICHOTE_API_HOST', '0.0.0.0')
port = getenv('MICHOTE_API_PORT', 5000)

@app.teardown_appcontext
def end_session(Exception):
    """Function called on session termination"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Function called when 404 not found error occurs"""
    return make_response(jsonify({'error':'not found'}), 404)

if __name__ == '__main__':
    """Launch the flask app form terminal"""
    app.run(host=host, port=port, threaded=True)
