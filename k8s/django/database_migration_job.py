from kubernetes import client

from resource import Resource


class DatabaseMigrationJob(Resource):
    def get(self):
        if not self.context.minikube:
            return
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
                            self.get_container()
                        ],
                        restart_policy='Never'
                    )
                ),
                backoff_limit=10,
                ttl_seconds_after_finished=0
            )
        )

    def get_container(self):
        return client.V1Container(
            name='django-app-migration',
            image=self.context.image,
            command=['python', 'manage.py', 'migrate'],
            env=[
                client.V1EnvVar(
                    name='DATABASE_URL',
                    value='postgres://dev_user:development@postgres-service:5432/dev_db'
                )
            ],
        )
