import os
from typing import List

from kubernetes import client

from resource import Resource


class Deployment(Resource):
    def get(self):
        (volumes, volume_mounts) = self.get_volumes() if self.context.minikube else (None, None)

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
                            self.get_container(volume_mounts)
                        ],
                        volumes=volumes
                    )
                )
            )
        )

    def get_container(self, volume_mounts: List[client.V1VolumeMount]):
        # We want to serve static files in development, i.e admin page
        command = [
            "python", "manage.py", "runserver", "0.0.0.0:8080"
        ] if self.context.minikube else None
        return client.V1Container(
            image=self.context.image,
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
                ),
                client.V1EnvVar(
                    name='RABBITMQ_PASSWORD',
                    value_from=client.V1EnvVarSource(
                        secret_key_ref=client.V1SecretKeySelector(
                            name='rabbitmq',
                            key='rabbitmq-password'
                        )
                    )
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

    def get_volumes(self):
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
