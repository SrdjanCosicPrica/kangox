from context import Context


class Resource:
    def __init__(self, context: Context):
        self.context = context

    def get(self):
        raise NotImplementedError
