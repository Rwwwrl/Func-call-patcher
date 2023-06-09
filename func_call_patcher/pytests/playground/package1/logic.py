from .second_logic import Dependency


def some_func(x=None) -> int:
    return 10


class Agreggator:
    @classmethod
    def some_classmethod(cls) -> int:
        return 10

    @staticmethod
    def some_statitcmethod() -> int:
        return 10


class RobotModel:
    def get_passport_value(self, x: int) -> int:
        return 10


class Robot:
    def __init__(self, robot_model: RobotModel):
        self.robot_model = robot_model

    def get_value(self) -> int:
        return self.robot_model.get_passport_value(x=10)

    @property
    def value(self) -> int:
        return 10


class SecondAggregator:
    def __init__(self):
        self.depedency = Dependency()
