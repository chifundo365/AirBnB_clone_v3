#!/usr/bin/python3
""" Index containing flask routes """
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """Shows the status of the api"""
    return jsonify({"status": "OK"})
