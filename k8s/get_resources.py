import argparse
import importlib
import json
import os
from typing import Type, List

from kubernetes import client

from context import Context
from resource import Resource


def get_resources(image: str, minikube: bool):
    path = os.path.abspath(os.path.dirname(__file__))
    context = Context(image, minikube)
    c = client.ApiClient()
    result = ''
    for directory in os.listdir(path):
        if not os.path.isdir(os.path.join(path, directory)):
            continue
        module = importlib.import_module(directory)
        try:
            resources: List[Type[Resource]] = module.resources
        except Exception:
            continue

        for klass in resources:
            data = klass(context).get()
            if data:
                result += json.dumps(c.sanitize_for_serialization(data))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str, help='Docker Image to deploy')
    parser.add_argument('--minikube', action='store_true', help='Setup for minikube')
    args = parser.parse_args()
    print(get_resources(args.image, args.minikube))
