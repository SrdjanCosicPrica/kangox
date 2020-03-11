from kubernetes import client


def get_service():
    return client.V1Service(
        api_version='v1',
        kind='Service',
        metadata=client.V1ObjectMeta(
            labels={
                'app': 'django-app'
            },
            name='django-app'
        ),
        spec=client.V1ServiceSpec(
            ports=[
                client.V1ServicePort(
                    protocol='TCP',
                    port=8080,
                    target_port=8080
                )
            ],
            selector={
                'app': 'django-app'
            }
        )
    )
