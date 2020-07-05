from typing import List, Type

from resource import Resource
from .database_migration_job import DatabaseMigrationJob
from .deployment import Deployment
from .ingress import Ingress
from .service import Service

resources: List[Type[Resource]] = [
    Deployment,
    Ingress,
    Service,
    DatabaseMigrationJob
]
