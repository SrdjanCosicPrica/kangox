class Context:
    def __init__(self, image: str = None, minikube: bool = False):
        self.image: str = image
        self.minikube: bool = minikube
