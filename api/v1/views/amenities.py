from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """ Retrivies a list of all the amenities """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_with_id(amenity_id):
    """ Retrievs a Amenity object with given id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False
    )
def delete_amenity(amenity_id):
    """ Deletes a Amenity object with given id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    elif data.get('name') is None:
        return "Missing name", 400
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not isinstance(data, dict):
            return "Not a JSON", 400
        for k, v in data.items():
            ignored_keys = ['id', 'created_at', 'updated_at']
            if k not in ignored_keys:
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
