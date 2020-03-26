from kubernetes import client

from resource import Resource


class Deployment(Resource):
    def get(self):
        return client.V1Deployment(
            api_version='apps/v1',
            kind='Deployment',
            metadata=client.V1ObjectMeta(
                name='postgres',
                labels={
                    'app': 'postgres'
                },
                namespace='default'
            ),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(
                    match_labels={
                        'app': 'postgres'
                    }
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={
                            'app': 'postgres'
                        }
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                image='postgres:11',
                                image_pull_policy='IfNotPresent',
                                name='postgres',
                                ports=[
                                    client.V1ContainerPort(
                                        container_port=5434
                                    )
                                ],
                                env=[
                                    client.V1EnvVar(
                                        name='POSTGRES_USER',
                                        value='dev_user'
                                    ),
                                    client.V1EnvVar(
                                        name='POSTGRES_PASSWORD',
                                        value='development'
                                    ),
                                    client.V1EnvVar(
                                        name='POSTGRES_DB',
                                        value='dev_db'
                                    )
                                ],
                                volume_mounts=[
                                    client.V1VolumeMount(
                                        name='postgres-volume-mount',
                                        mount_path='/var/lib/postgresql/data'
                                    )
                                ]
                            )
                        ],
                        volumes=[
                            client.V1Volume(
                                name='postgres-volume-mount',
                                persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                    claim_name='postgres-pvc'
                                )
                            )
                        ]
                    )
                )
            )
        )
