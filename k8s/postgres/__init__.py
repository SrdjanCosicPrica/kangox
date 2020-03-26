from typing import List, Type

from resource import Resource
from .deployment import Deployment
from .persistent_volume import PersistentVolume
from .persistent_volume_claim import PersistentVolumeClaim
from .service import Service

resources: List[Type[Resource]] = [
    Deployment,
    Service,
    PersistentVolume,
    PersistentVolumeClaim
]
