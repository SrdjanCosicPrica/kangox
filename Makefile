IMAGE_REPOSITORY=kangox
.PHONY: image
.SILENT: minikube-check virtualbox-check environment image config
.DEFAULT_GOAL: environment

environment: image config

image: minikube-check
	$(eval LATEST_IMAGE=$(shell sh -c 'eval $$(minikube docker-env) && docker images $(IMAGE_REPOSITORY) --format "{{ .Tag }}" | sort -nr | head -n1'))
	$(eval IMAGE=$(shell echo $$(($(LATEST_IMAGE) + 1))))
	echo "Building image: $(IMAGE_REPOSITORY):$(IMAGE)"
	eval $$(minikube docker-env); \
	docker build . -t "$(IMAGE_REPOSITORY):$(IMAGE)"

config: minikube-check
	if [ -z "$(IMAGE)" ]; then\
	    $(eval IMAGE=$(shell sh -c 'eval $$(minikube docker-env) && docker images $(IMAGE_REPOSITORY) --format "{{ .Tag }}" | sort -nr | head -n1'))\
	    echo "Using existing image $(IMAGE_REPOSITORY):$(IMAGE)";\
	fi
	echo "Applying resources to cluster\n"
	python k8s/apply_resources.py $(IMAGE_REPOSITORY):$(IMAGE) --dev | kubectl apply -f - --force

minikube-check: virtualbox-check
	$(eval MINIKUBE_VERSION=$(shell minikube version))
	if [ -z "$(MINIKUBE_VERSION)" ]; then\
		echo 'Minikube is not installed.' && exit 1;\
	fi
	echo 'Minikube version $(MINIKUBE_VERSION)'
	$(eval STATUS=$(shell minikube status | awk '/host/ {print $$2}'))
	if [ "$(STATUS)" == 'Stopped' ] || [ -z "$(STATUS)" ]; then\
	    echo 'Minkube is not running. Starting...';\
	    minikube start --vm-driver virtualbox --feature-gates TTLAfterFinished=true;\
	fi
	$(minikube addons enable ingress)

virtualbox-check:
	$(eval VIRTUALBOX_VERSION=$(shell vboxmanage --version))
	if [ -z "$(VIRTUALBOX_VERSION)" ]; then\
		echo 'Virtualbox is not installed.' && exit 1;\
	fi
	echo 'Virtualbox version $(VIRTUALBOX_VERSION)'
