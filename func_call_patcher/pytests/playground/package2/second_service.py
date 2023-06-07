from func_call_patcher.pytests.playground.package1 import logic


def service_func():
    # КЕЙС 0
    # что патчим: some_func
    # проверка юз кейса, когда логика (some_func) вызывается внутри функции
    # при этом импорт выглядит как from path import module
    return logic.some_func(x=10)
