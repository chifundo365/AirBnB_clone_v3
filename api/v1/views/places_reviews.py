#!/usr/bin/python3
"""
view for the reviews of places
"""
from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        "/places/<place_id>/reviews",
        methods=["GET"],
        strict_slashes=False
        )
def get_place_reviews(place_id):
    """Retrivies all the Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews]), 200


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET"],
        strict_slashes=False
        )
def get_review(review_id):
    """ Retrivies a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route(
        "reviews/<review_id>",
        methods=["DELETE"],
        strict_slashes=False
        )
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route(
        "places/<place_id>/reviews",
        methods=["POST"],
        strict_slashes=False
        )
def create_review(place_id):
    """ Creates a Review object of a particular place """
    place = storage.get(Place, place_id)
    if not place:
        print(place_id)
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return "Not a JSON", 400
    elif "user_id" not in data.keys():
        return "Missing user_id", 400
    elif "text" not in data.keys():
        return "Missing text", 400
    else:
        user = storage.get(User, data.get("user_id"))
        if not user:
            abort(404)

        review = Review(**data)
        setattr(review, "place_id", place_id)
        review.user_id = user.id
        storage.new(review)
        storage.save()
        storage.reload()

        return jsonify(review.to_dict()), 201


@app_views.route("reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400

    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    storage.reload()
    return jsonify(review.to_dict()), 200
