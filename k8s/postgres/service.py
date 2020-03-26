from kubernetes import client

from resource import Resource


class Service(Resource):
    def get(self):
        return client.V1Service(
            kind='Service',
            api_version='v1',
            metadata=client.V1ObjectMeta(
                labels={
                    'app': 'postgres'
                },
                name='postgres-service'
            ),
            spec=client.V1ServiceSpec(
                ports=[
                    client.V1ServicePort(
                        protocol='TCP',
                        port=5432,
                        target_port=5432
                    )
                ],
                selector={
                    'app': 'postgres'
                }
            )
        )
