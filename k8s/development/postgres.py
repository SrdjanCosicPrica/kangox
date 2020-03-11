from kubernetes import client


def get_persistent_volume():
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


def get_persistent_volume_claim():
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


def get_database():
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


def get_service():
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
