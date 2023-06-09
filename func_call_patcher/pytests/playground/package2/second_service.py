from func_call_patcher.pytests.playground.package1 import logic


def case_1():
    # КЕЙС _1
    # что патчим: some_func
    # проверка юз кейса, когда логика (some_func) вызывается внутри функции
    # при этом импорт выглядит как from path import module
    return logic.some_func(x=10)


def case_2():
    # КЕЙС _2
    # что патчим: .Agreggator.some_classmethod
    # проверка юз кейса, когда логика является методом класса
    # при этом импорт выглядит как from path import module
    return logic.Agreggator.some_classmethod()
