def some_func(x=None) -> int:
    return 10


class Agreggator:
    def execute() -> int:
        return 10


class RobotModel:
    def get_passport_value(self, x: int) -> int:
        return 10


class Robot:
    def __init__(self, robot_model: RobotModel):
        self.robot_model = robot_model

    def get_value(self) -> int:
        return self.robot_model.get_passport_value(x=10)
