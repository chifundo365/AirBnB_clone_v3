#!/usr/bin/python3
"""Starts a Flask web application. Registers a blueprint"""
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_current_session(excp):
    """Closes sqlalchemy current session"""
    storage.close()


@app.errorhandler(404)
def not_found_json(err):
    """ Returns an object indicating 404-not found error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    if host is None:
        host = "0.0.0.0"

    if port is None:
        port = 5000

    app.run(port=port, host=host, threaded=True)
