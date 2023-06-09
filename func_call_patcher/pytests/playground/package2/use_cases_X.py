from func_call_patcher.pytests.playground.package1 import src1


class Case_1:
    @classmethod
    def run(cls):
        # КЕЙС _1
        # что патчим: some_func
        # проверка юз кейса, когда логика (some_func) вызывается внутри функции
        # при этом импорт выглядит как from path import module
        return src1.some_func(x=10)


class Case_2:
    @classmethod
    def run(cls):
        # КЕЙС _2
        # что патчим: .Agreggator.some_classmethod
        # проверка юз кейса, когда логика является методом класса
        # при этом импорт выглядит как from path import module
        return src1.Agreggator.some_classmethod()
