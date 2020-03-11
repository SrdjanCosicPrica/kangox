import json

from kubernetes import client

from .django_app import get_service


def get_services():
    c = client.ApiClient()
    json_data = json.dumps(c.sanitize_for_serialization(get_service()))
    return json_data
