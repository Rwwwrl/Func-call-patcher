from .src3 import Dependency as src3_Dependency


class Dependency:
    def __init__(self):
        self.dependency = src3_Dependency()

    @property
    def some_property(self):
        return 10

    def some_method(self, x: int, y: int):
        return 10
