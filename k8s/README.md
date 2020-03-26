# Kubernetes

## Get Resources
In order to get the resources to add to the cluster, you call the `get_resources.py`
file with some arguments.

```shell script
python get_resources.py
```
#### Arguments
| Argument | Type    | Description                                                       | Example  | Default |
|----------|---------|-------------------------------------------------------------------|----------|---------|
| image    | string  | A docker image repository and tag                                 | kangox:1 |         |
| minikube | boolean | Determines if the resources will be applied to a minikube cluster |          | false   |

## Contributing
`get_resources.py` will traverse the `k8s` directory and look for python modules
that export a variable named `resources`. The `resources` variable must contain
a list of `Resource` classes.

Eg.
```
k8s
    - module/
        __init__.py
        deployment.py

# module.__init__.py
from .deployment import Deployment

resources = [
    Deployment
]
```

Each resource class must inherit from the base `Resource` class.
The class accepts a `Context` as primary argument, which contains
configuration options.
See `resource.py` and `context.py`.
