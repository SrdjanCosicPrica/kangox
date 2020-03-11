from kubernetes import client


def get_nginx_ingress():
    return client.NetworkingV1beta1Ingress(
        api_version='networking.k8s.io/v1beta1',
        kind='Ingress',
        metadata=client.V1ObjectMeta(
            name='ingress-django-app',
            annotations={
                'kubernetes.io/ingress.class': 'nginx'
            }
        ),
        spec=client.NetworkingV1beta1IngressSpec(
            rules=[
                client.NetworkingV1beta1IngressRule(
                    host='local.kangox.com',
                    http=client.NetworkingV1beta1HTTPIngressRuleValue(
                        paths=[
                            client.NetworkingV1beta1HTTPIngressPath(
                                path='/',
                                backend=client.NetworkingV1beta1IngressBackend(
                                    service_name='django-app',
                                    service_port=8080
                                )
                            )
                        ]
                    )
                )
            ]
        )
    )
