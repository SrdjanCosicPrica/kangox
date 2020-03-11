# KangoX
Kubernetes, Django and Nginx all together for a new project.

## Requirements
```
python >= 3.7
```

## Installation
1. [Install Minikube together with VirtualBox and Kubectl](https://kubernetes.io/docs/tasks/tools/install-minikube/)
1. Install k8s requirements (Virtual environment recommended)
    ```
    pip3 install -r k8s/requirements.txt
    ```
1. Run make
    ```
    make
    ```
1. The ingress is configured for **local.kangox.com** via the minikube ip, add it to
your **/etc/hosts** 
    ```
    echo "$(minikube ip) local.kangox.com" | sudo tee -a /etc/hosts
    ````
1. Check the state of the deployments and pods in the minikube dashboard
    ```
    minikube dashboard
    ```
    It can take a few minutes for all the deployments to turn green. The important part
    is that the postgres deployment becomes green and the database migration job is
    removed. No jobs should exist.
1. Create a superuser
    ```
    kubectl exec django-app<id> python manage.py createsuperuser -it
    ```

You can now access `local.kangox.com/admin/` in your browser.

## Troubleshooting
#### Minikube
If you lose data from postgres, make sure that the storage-provisioner in minikube is in Running state
```
kubectl get pods -A
```
If it's not running or in a CrashLoopBackOff, delete minikube and execute
```
rm ~/.minikube/cache/images/gcr.io/k8s-minikube/storage-provisioner_v1.8.1
```
See https://github.com/kubernetes/minikube/issues/6246

#### Cannot reach the service
1. Check that the deployments are OK in the dashboard
    ```
    minikube dashboard
    ```
1. Make sure that the ingress is enabled for minikube (the `make` script should handle this)
    ```
    minikube addons enable ingress
    ```
1. Make sure that the minikube ip only has one entry in your **/etc/hosts** file
    ```
    cat /etc/hosts
    ```
   If minikube ip does not exist or is wrong, delete the old entry and run
   ```
   echo "$(minikube ip) local.kangox.com" | sudo tee -a /etc/hosts
   ```

## Updating the local image
Sometimes you need to add or upgrade a package in requirements, and that means
you also need to update the image.

You can achieve this by simply running the make script.
```
make
```

## Updating kubernetes configuration without building a new image
```
make config
```

## Considerations
* Pipeline should have 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.27.1/deploy/static/mandatory.yaml
```

* Cloud Provider configuration steps for Nginx-Ingress
https://kubernetes.github.io/ingress-nginx/deploy/#provider-specific-steps

