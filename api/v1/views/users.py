from flask import Flask, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """ Retrievies a list of all user objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User obj  with a given id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object with given id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a User object """
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    elif data.get("email") is None:
        return "Missing email", 400
    elif data.get("password") is None:
        return "Missing password", 400
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ updates a User object with given id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    for k, v in data.items():
        disallowed_keys = ['id', 'email', 'created_at', 'updated_at']
        if k not in disallowed_keys:
            setattr(user, k, v)
    return jsonify(user.to_dict()), 200
