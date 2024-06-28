#!/usr/bin/python3
""" Creates a new view for cities """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    "/states/<state_id>/cities",
    methods=["GET"],
    strict_slashes=False
    )
def get_state_cities(state_id):
    """
    Retrivies the list of all the City objects of a state

    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_with_id(city_id):
    """ Returns a json repre. of a city with given id """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city  with a given city_id """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"],
    strict_slashes=False
    )
def create_city(state_id):
    """ Creates a City  object which is linked to a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    elif data.get("name") is None:
        return "Missing name", 400

    new_city = City(**data)
    storage.new(new_city)
    setattr(new_city, 'state_id', state.id)
    storage.save()
    storage.reload()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        print(data)
        return "Not a JSON", 400
    for key, value in data.items():
        ignored_keys = ['state_id', 'id', 'created_at', 'updated_at']
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
