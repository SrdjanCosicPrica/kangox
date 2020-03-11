import argparse

from deployments import get_deployments
from development import get_development_resources
from ingress import get_ingresses
from services import get_services


def apply_resources(image, development):
    json_data = get_deployments(image, development) + get_services() + get_ingresses()
    if development:
        json_data += get_development_resources(image)

    return json_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str, help='Docker Image to deploy')
    parser.add_argument('--dev', action='store_true', help='Setup for local development')
    args = parser.parse_args()
    print(apply_resources(args.image, args.dev))
