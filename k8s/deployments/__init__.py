import json

from kubernetes import client

from .django_app import get_django_deployment


def get_deployments(image, development):
    c = client.ApiClient()
    json_data = json.dumps(c.sanitize_for_serialization(
        get_django_deployment(image, development)
    ))
    return json_data
