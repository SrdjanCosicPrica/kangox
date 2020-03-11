import os

from kubernetes import client


def get_volumes():
    """
    Volumes needed for hot-reload in development
    """
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    volumes = [
        client.V1Volume(
            name='reload',
            host_path=client.V1HostPathVolumeSource(
                path=os.path.join(project_root, 'src'),
                type='Directory'
            )
        )
    ]
    volume_mounts = [
        client.V1VolumeMount(
            name='reload',
            mount_path='/src'
        )
    ]
    return volumes, volume_mounts


def get_django_deployment(image, development=False):
    (volumes, volume_mounts) = get_volumes() if development else (None, None)
    # We want to serve static files in development, i.e admin page
    command = ["python", "manage.py", "runserver", "0.0.0.0:8080"] if development else None
    return client.V1Deployment(
        api_version='apps/v1',
        kind='Deployment',
        metadata=client.V1ObjectMeta(
            name='django-app',
            labels={
                'app': 'django-app'
            },
            namespace='default'
        ),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={
                    'app': 'django-app'
                }
            ),
            revision_history_limit=3,
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={
                        'app': 'django-app'
                    }
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            image=image,
                            image_pull_policy='IfNotPresent',
                            name='django-app',
                            ports=[
                                client.V1ContainerPort(
                                    container_port=8080
                                )
                            ],
                            command=command,
                            volume_mounts=volume_mounts,
                            env=[
                                client.V1EnvVar(
                                    name='DATABASE_URL',
                                    value='postgres://dev_user:development@postgres-service:5432/dev_db'
                                ),
                                client.V1EnvVar(
                                    name='ALLOWED_HOSTS',
                                    value='.kangox.com,127.0.0.1,[::1],localhost'
                                )
                            ],
                            readiness_probe=client.V1Probe(
                                http_get=client.V1HTTPGetAction(
                                    path='/ping/',
                                    port=8080,
                                    http_headers=[
                                        client.V1HTTPHeader(
                                            name='Host',
                                            value='127.0.0.1'
                                        )
                                    ]
                                ),
                                period_seconds=5,
                                initial_delay_seconds=5,
                                failure_threshold=1,
                            ),
                            liveness_probe=client.V1Probe(
                                http_get=client.V1HTTPGetAction(
                                    path='/ping/',
                                    port=8080,
                                    http_headers=[
                                        client.V1HTTPHeader(
                                            name='Host',
                                            value='127.0.0.1'
                                        )
                                    ]
                                ),
                                period_seconds=5,
                                initial_delay_seconds=5,
                                failure_threshold=1
                            )
                        )
                    ],
                    volumes=volumes
                )
            )
        )
    )
