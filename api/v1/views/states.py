#!/usr/bin/python3
""" Creates a new view for states """
from flask import jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """
    Get all the states objects in storage
    Returns a list of dictionary_represeentations of the objects
    """
    states = storage.all(State).values()
    states_dict_list = [state.to_dict() for state in states]
    return jsonify(states_dict_list), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_with_id(state_id):
    """ Returns a json repre. of a state with given id """
    state = storage.get(State, state_id)
    if state:
        return state.to_dict(), 200
    abort(404)


@app_views.route(
    "/states/<state_id>",
    methods=["DELETE"],
    strict_slashes=False
    )
def delete_state(state_id):
    """ Deletes a state with a given stated_id """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a state  object"""
    headers = request.headers

    if headers.get('Content-Type') != 'application/json':
        return "Not a JSON", 400
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400

    if not isinstance(data, dict):
        return "Not a JSON", 400
    elif data.get("name") is None:
        return "Missing name", 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    storage.reload()
    print(storage.get(State, new_state.id))
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ Updates attributes of a state object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400

    if not isinstance(data, dict):
        return "Not a JSON", 400
    for key, value in data.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
