import json

from kubernetes import client

from ingress.nginx_ingress import get_nginx_ingress


def get_ingresses():
    c = client.ApiClient()
    json_data = json.dumps(c.sanitize_for_serialization(get_nginx_ingress()))
    return json_data
