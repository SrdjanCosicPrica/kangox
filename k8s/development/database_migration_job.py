from kubernetes import client


def get_database_migration_job(image):
    return client.V1Job(
        api_version='batch/v1',
        kind='Job',
        metadata=client.V1ObjectMeta(
            name='database-migration-job'
        ),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name='django-app-migration',
                            image=image,
                            command=['python', 'manage.py', 'migrate'],
                            env=[
                                client.V1EnvVar(
                                    name='DATABASE_URL',
                                    value='postgres://dev_user:development@postgres-service:5432/dev_db'
                                )
                            ],
                        ),
                    ],
                    restart_policy='Never'
                )
            ),
            backoff_limit=10,
            ttl_seconds_after_finished=0
        )
    )
