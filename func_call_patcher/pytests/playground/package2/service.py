from func_call_patcher.pytests.playground.package1.logic import (
    Agreggator,
    Robot,
    RobotModel,
    SecondAggregator,
    some_func,
    some_func_with_decorator_on_it,
)

# КЕЙС 1
# проверка юз кейса, когда логика (some_func) вызывается при чтении файла
some_func()


def service_func():
    # КЕЙС 2
    # что патчим: some_func
    # проверка юз кейса, когда логика (some_func) вызывается внутри функции
    # при этом импорт выглядит как from path.module import func
    return some_func(x=10)


class Some:
    def __init__(self):
        # КЕЙС 3
        # что патчим: some_func
        # проверка юз кейса, когда логика (some_func) вызывается внутри метода класса
        some_func()


def another_service_func():
    def inner():
        # КЕЙС 4
        # что патчим: some_func
        # проверка юз кейса, когда логика (some_func) вызывается внутри нескольких функций
        some_func()

    return inner


def classmethod_execute():
    # КЕЙС 5
    # что патчим: Agreggator.some_classmethod
    # проверка юз кейса, когда логика (.execute) является @classmethod
    return Agreggator.some_classmethod()


robot_model = RobotModel()
robot = Robot(robot_model=robot_model)


def instancemethod_execute():
    # КЕЙС 6
    # что патчим: RobotModel.get_passport_value
    # проверка юз кейса, когда логика (.get_passport_value) является инстанс методом
    return robot_model.get_passport_value(x=10)


def instancemethod_execute2():
    # КЕЙС 7
    # что патчим: RobotModel.get_passport_value
    # проверка юз кейса, когда логика (.get_passport_value) вызывается внутри другого инстанс метода
    return robot.get_value()


def func_to_patch_in_executed_module():
    return 10


def outer_func_to_patch_in_executed_module():
    # КЕЙС 8
    # что патчим: func_to_patch_in_executed_module
    # проверка юз кейса, когда логика (func_to_patch_in_executed_module) в самом запускаемом модуле
    return func_to_patch_in_executed_module()


class SomeClass:
    def func_to_patch_in_executed_module(self):
        return 10

    def outer_func_to_patch_in_executed_module(self):
        # КЕЙС 9
        # что патчим: .func_to_patch_in_executed_module
        # проверка юз кейса, когда логика (.func_to_patch_in_executed_module) в самом запускаемом модуле,
        # в том же классе
        return self.func_to_patch_in_executed_module()


def case10():
    # КЕЙС 10
    # что патчим: Robot.value
    # проверка юз кейса, где что мы патчим является свойством
    return robot.value


def case11():
    # КЕЙС 11
    # что патчим: Dependency.some_property
    # проверка юз кейса, где мы патчим свойство (по цепочке)
    return SecondAggregator().depedency.some_property


def case12():
    # КЕЙС 12
    # что патчим: Dependency.some_method
    # проверка юз кейса, где мы патчим свойство (по цепочке)
    return SecondAggregator().depedency.some_method(x=10, y=20)


def case13():
    # КЕЙС 13
    # что патчим: Agreggator.some_statitcmethod
    # проверка юз кейса, когда логика (.some_statitcmethod) является или @staticmethod
    return Agreggator.some_statitcmethod()


def case14():
    # КЕЙС 14
    # что патчим: Agreggator.some_statitcmethod
    # проверка юз кейса, что декоратор на методе не повлияет на работу патча
    return Agreggator().some_method_with_decorator_on_it()


def case15():
    # КЕЙС 15
    # что патчим: Agreggator.some_property_with_decorator_on_it
    # проверка юз кейса, что декоратор на свойстве не повлияет на работу патча
    return Agreggator().some_property_with_decorator_on_it


def case16():
    # КЕЙС 16
    # что патчим: some_func_with_decorator_on_it
    # проверка юз кейса, что декоратор на функции никак не повлияет на работу патча
    return some_func_with_decorator_on_it()
