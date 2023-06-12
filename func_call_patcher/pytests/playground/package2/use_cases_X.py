from func_call_patcher.pytests.playground.package1 import src1

robot_model = src1.RobotModel()
robot = src1.Robot(robot_model=robot_model)


def local_func():
    return 10


# КЕЙС 1
# проверка юз кейса, когда логика (some_func) вызывается при чтении файла
src1.some_func()


class Case_2:
    @classmethod
    def run(cls):
        # КЕЙС 2
        # что патчим: some_func
        # проверка юз кейса, когда логика (some_func) вызывается внутри функции
        # при этом импорт выглядит как from path.module import func
        return src1.some_func(x=10)


class Case_3:
    class Some:
        def __init__(self):
            # КЕЙС 3
            # что патчим: some_func
            # проверка юз кейса, когда логика (some_func) вызывается внутри метода класса
            src1.some_func()

    @classmethod
    def run(cls):
        return cls.Some()


class Case_4:
    @classmethod
    def run(cls):
        def inner():
            # КЕЙС 4
            # что патчим: some_func
            # проверка юз кейса, когда логика (some_func) вызывается внутри нескольких функций
            src1.some_func()

        return inner()


class Case_5:
    @classmethod
    def run(cls):
        # КЕЙС 5
        # что патчим: Agreggator.some_classmethod
        # проверка юз кейса, когда логика (.execute) является @classmethod
        return src1.Agreggator.some_classmethod()


class Case_6:
    @classmethod
    def run(cls):
        # КЕЙС 6
        # что патчим: RobotModel.get_passport_value
        # проверка юз кейса, когда логика (.get_passport_value) является инстанс методом
        return robot_model.get_passport_value(x=10)


class Case_7:
    @classmethod
    def run(cls):
        # КЕЙС 7
        # что патчим: RobotModel.get_passport_value
        # проверка юз кейса, когда логика (.get_passport_value) вызывается внутри другого инстанс метода
        return robot.get_value()


class Case_8:
    @classmethod
    def run(cls):
        # КЕЙС 8
        # что патчим: local_func
        # проверка юз кейса, когда логика (local_func) находится в самом запускаемом модуле
        return local_func()


class Case_9:
    class SomeClass:
        def src_func(self):
            return 10

        def to_run_func(self):
            # КЕЙС 9
            # что патчим: .src_func
            # проверка юз кейса, когда логика (.src_func) в самом запускаемом модуле,
            # в том же классе
            return self.src_func()

    @classmethod
    def run(cls):
        return cls.SomeClass().to_run_func()


class Case_10:
    @classmethod
    def run(cls):
        # КЕЙС 10
        # что патчим: Robot.value
        # проверка юз кейса, где то что мы патчим является свойством
        return robot.value


class Case_11:
    @classmethod
    def run(cls):
        # КЕЙС 11
        # что патчим: Dependency.some_property
        # проверка юз кейса, где мы патчим свойство (по цепочке)
        return src1.SecondAggregator().depedency.some_property


class Case_12:
    @classmethod
    def run(cls):
        # КЕЙС 12
        # что патчим: Dependency.some_method
        # проверка юз кейса, где мы патчим метод (по цепочке)
        return src1.SecondAggregator().depedency.some_method(x=10, y=20)


class Case_13:
    @classmethod
    def run(cls):
        # КЕЙС 13
        # что патчим: Agreggator.some_statitcmethod
        # проверка юз кейса, когда логика (.some_statitcmethod) является или @staticmethod
        return src1.Agreggator.some_statitcmethod()


class Case_14:
    @classmethod
    def run(cls):
        # КЕЙС 14
        # что патчим: Agreggator.some_statitcmethod
        # проверка юз кейса, что декоратор на методе не повлияет на работу патча
        return src1.Agreggator().some_method_with_decorator_on_it()


class Case_15:
    @classmethod
    def run(cls):
        # КЕЙС 15
        # что патчим: Agreggator.some_property_with_decorator_on_it
        # проверка юз кейса, что декоратор на свойстве не повлияет на работу патча
        return src1.Agreggator().some_property_with_decorator_on_it


class Case_16:
    @classmethod
    def run(cls):
        # КЕЙС 16
        # что патчим: some_func_with_decorator_on_it
        # проверка юз кейса, что декоратор на функции никак не повлияет на работу патча
        return src1.some_func_with_decorator_on_it()


class Case_17:
    @classmethod
    def run(cls):
        # КЕЙС 17
        # что патчим Dependency.some_property
        # проверка из кейса патча свойства в более длинной цепочке
        return src1.SecondAggregator().depedency.dependency.some_property


class Case_18:
    @classmethod
    def run(cls):
        from func_call_patcher.pytests import playground

        # КЕЙС 18
        # что патчим some_func
        # проверка из кейса, где функция вызывается по цепочке из нескольких модулей
        return playground.package1.src1.some_func()


class Case_19:
    @classmethod
    def run(cls):
        # КЕЙС 19
        # что патчим Robot.base_robot_method
        # проверка из кейса, где метод определен не в самом классе, а в его родителе

        return robot.base_robot_method()
