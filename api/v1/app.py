#!/usr/bin/python3
"""Starts a Flask web application. Registers a blueprint"""
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_current_session(excp):
    """Closes sqlalchemy current session"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port  = getenv("HBNB_API_PORT")

    if host is None:
        host = "0.0.0.0"

    if port is None:
        port = 5000

    app.run(port=port, host=host, threaded=True)


