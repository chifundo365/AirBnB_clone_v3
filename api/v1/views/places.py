#!/usr/bin/python3
"""
Contains Places view
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET"],
    strict_slashes=False
    )
def get_places(city_id):
    """ Retrievies a list of all Place objects of a City """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places]), 200


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place obj  with a given id """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route(
    "/places/<place_id>",
    methods=["DELETE"],
    strict_slashes=False
    )
def delete_place(place_id):
    """ Deletes a Place object with given id """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route(
    "/cities/<city_id>/places",
    methods=["POST"],
    strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    elif data.get("user_id") is None:
        return "Missing user_id", 400
    elif storage.get(User, data.get("user_id")) is None:
        abort(404)
    elif data.get("name") is None:
        return "Missing name", 400
    place = Place(**data)
    setattr(place, "city_id", city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ updates a Place object with given id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    for k, v in data.items():
        ignored_k = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if k not in ignored_k:
            setattr(place, k, v)
    storage.save()
    storage.reload()
    return jsonify(place.to_dict()), 200
