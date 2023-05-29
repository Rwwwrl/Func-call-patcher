from func_call_patcher.pytests.playground.package1.logic import Agreggator, Robot, RobotModel, some_func

# проверка юз кейса, когда логика (some_func) вызывается при чтении файла
some_func()


def service_func():
    # что патчим: some_func
    # проверка юз кейса, когда логика (some_func) вызывается внутри функции
    # при этом импорт выглядит как from path.module import func
    return some_func(x=10)


class Some:
    def __init__(self):
        # что патчим: some_func
        # проверка юз кейса, когда логика (some_func) вызывается внутри метода класса
        some_func()


def another_service_func():
    def inner():
        # что патчим: some_func
        # проверка юз кейса, когда логика (some_func) вызывается внутри нескольких функций
        some_func()

    return inner


def classmethod_execute():
    # что патчим: Agreggator.execute
    # проверка юз кейса, когда логика (.execute) является @classmethod или @staticmethod
    return Agreggator.execute()


robot_model = RobotModel()
robot = Robot(robot_model=robot_model)


def instancemethod_execute():
    # что патчим: RobotModel.get_passport_value
    # проверка юз кейса, когда логика (.get_passport_value) является инстанс методом
    return robot_model.get_passport_value(x=10)


def instancemethod_execute2():
    # что патчим: RobotModel.get_passport_value
    # проверка юз кейса, когда логика (.get_passport_value) вызывается внутри другого инстанс метода
    return robot.get_value()
