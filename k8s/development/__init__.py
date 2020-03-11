import json

from kubernetes import client

from .database_migration_job import get_database_migration_job
from .postgres import (
    get_database,
    get_persistent_volume,
    get_persistent_volume_claim,
    get_service as get_postgres_service
)


def get_development_resources(image):
    c = client.ApiClient()
    json_data = json.dumps(c.sanitize_for_serialization(get_persistent_volume()))
    json_data += json.dumps(c.sanitize_for_serialization(get_persistent_volume_claim()))
    json_data += json.dumps(c.sanitize_for_serialization(get_database()))
    json_data += json.dumps(c.sanitize_for_serialization(get_postgres_service()))
    json_data += json.dumps(c.sanitize_for_serialization(get_database_migration_job(image)))
    return json_data
