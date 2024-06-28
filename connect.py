#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ GET /api/v1/users/<amenity_id>
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/users/{}".format("doesn_t_exist"))
    print(r.status_code)
