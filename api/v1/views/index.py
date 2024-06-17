#!/usr/bin/python3

from flask import jsonfy
from api.v1.views import app_views

@app_views.route("/status")
def status():
    """Shows the status of the api"""
    return jsonfy({"status": "OK"})
