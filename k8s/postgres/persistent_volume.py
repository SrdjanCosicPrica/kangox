from kubernetes import client

from resource import Resource


class PersistentVolume(Resource):
    def get(self):
        return client.V1PersistentVolume(
            kind='PersistentVolume',
            api_version='v1',
            metadata=client.V1ObjectMeta(
                name='postgres-pv',
                labels={
                    'pv': 'postgres'
                }
            ),
            spec=client.V1PersistentVolumeSpec(
                storage_class_name='manual',
                capacity={
                    'storage': '2Gi'
                },
                access_modes=['ReadWriteOnce'],
                host_path=client.V1HostPathVolumeSource(
                    path='/data/postgres_storage'
                )
            )
        )
