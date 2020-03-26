from kubernetes import client

from resource import Resource


class PersistentVolumeClaim(Resource):
    def get(self):
        return client.V1PersistentVolumeClaim(
            kind='PersistentVolumeClaim',
            api_version='v1',
            metadata=client.V1ObjectMeta(
                name='postgres-pvc',
                labels={
                    'pvc': 'postgres'
                }
            ),
            spec=client.V1PersistentVolumeClaimSpec(
                storage_class_name='manual',
                access_modes=['ReadWriteOnce'],
                resources=client.V1ResourceRequirements(
                    requests={
                        'storage': '2Gi'
                    }
                ),
                volume_name='postgres-pv'
            )
        )
