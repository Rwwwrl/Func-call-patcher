from typing import Optional
from uuid import uuid4

from . import hints
from .patcher import FuncPatcher, MethodPatcherFacade
from .utils import Path


class FuncCallPatcher:
    def __init__(
        self,
        path_to_func_in_executable_module: str,
        line_number_where_func_executed: int,
        decorator_inner_func: hints.DecoratorInnerFunc,
        is_method: bool,
        relationship_identifier: Optional[hints.RelationshipIdentifier] = None,
    ):
        """
        Задачей данного FuncPatcher`а является запатчить один конкретный вызов функции/метода в запускаемом модуле.

        *запускаемый* модуль - модуль, в котором запускается функция/метод, которую мы хотим пропатчить

        Пусть у нас есть такая структура проекта

        ├── package1
        │   └── logic.py
        ├── package2
        │   └── service.py
        └── run.py

        # содержимое файлов:

        # logic.py

        def some_func(x=None) -> int:
            return 10

        # service.py

        # 1. делаем импорт функции из модуля
        # from package1.logic import some_func

        # 2. импортируем модуль
        from package1 import logic


        def service_func():
            # при 1-ом варианте импорта
            # return some_func(x=10)    # номер линии 10

            # при 2-ом варианте импорта
            return logic.some_func(x=10)    # номер линии 13


        :param path_to_func_in_executable_module - полный путь до функции, которую мы хотим запатчить в запускаемом
          модуле.
            Из примера выше:
                мы хотим запатчить функцию logic.some_func внутри service.service_func . В таком случае запускаемый
                модуль это service.py, а полный путь до функции зависит от варианта импорта:
                    для 1-ого варианта это "package2.service.some_func"
                    для 2-ого варианта это "package2.service.logic.some_func"

        :param line_number_where_func_executed - мы бы не хотели патчить все вызова функции some_func, а только тот,
          который находится на линии с номером line_number_where_func_executed в запускаемом модуле
            Из примера выше:
                мы хотим запатчить функцию logic.some_func внутри service.service_func. В зависимости от импорта
                line_number_where_func_executed равен:
                    для 1-ого варианта это 5
                    для 2-ого варианта это 8

        :param decorator_inner_func - функция, которая оборачивает вызов функции, которую мы патчим
            пример decorator_inner_func:

            def decorator_inner_func(func, func_args, func_kwargs, frame: FrameType):
                :param func - это сама функция, которую мы патчим, как объект
                :param func_args - позиционный аргументы, с которыми это функция бы запустилась
                :param func_args - именованные аргументы, с которыми это функция бы запустилась
                :param frame: FrameType - объект из types, который ранее определили в FuncCallPatcher, нужен если вдруг
                  нужна будет информация из него

        :param is_method - с помощью FuncCallPatcher можно запатчить не только вызов функции, но также и метода.
            логика тут та же: указываем полный путь до запускаемого модуля до класса и метода,
                в котором находится нужный метод

            Пример path_to_func_in_executable_module, если is_method = True:
                path_to_func_in_executable_module = "playground.package2.service.Agreggator.execute"

        :param relationship_identifier - идентификтор взаимосвязаннсти, если два идентификтора были запущены в рамках
          одного процесса, то они должны иметь один и тот же идентификатор.

        Пример использования патча для патчирования вызова some_func внутри package2.service из примера выше:

        # run.py
        from package2 import service

        from func_call_patcher import FuncCallPatcher


        def decorator_inner_func(func, func_args, func_kwargs, frame):
            print(f'func_args = {func_args}, func_kwargs = {func_kwargs}')
            return func(*func_args, **func_kwargs)


        func_call_patcher = FuncCallPatcher(
            # path_to_func_in_executable_module='package2.service.some_func',
            path_to_func_in_executable_module='package2.service.logic.some_func',
            line_number_where_func_executed=13,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            result = service.service_func()

        Посмотреть на остальные сценарии использования можно в func_call_patcher/pytest/func_call_patcher.py
        """

        if not relationship_identifier:
            relationship_identifier = uuid4()

        if is_method:
            path = Path(path=path_to_func_in_executable_module, is_path_to_method=True)
            self._patcher = MethodPatcherFacade(
                path_to_func_in_executable_module=path,
                line_number_where_func_executed=line_number_where_func_executed,
                decorator_inner_func=decorator_inner_func,
                relationship_identifier=relationship_identifier,
            )
        else:
            path = Path(path=path_to_func_in_executable_module, is_path_to_method=False)
            self._patcher = FuncPatcher(
                path_to_func_in_executable_module=path,
                line_number_where_func_executed=line_number_where_func_executed,
                decorator_inner_func=decorator_inner_func,
                relationship_identifier=relationship_identifier,
            )

    def __enter__(self):
        self._patcher.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        self._patcher.__exit__(*args, **kwargs)


class MultiFuncCallPatcher:
    """
    класс нужен для случая, когда нужно пропатчить сразу несколько вызовов.
    Вместо того чтобы писать
    with func_patcher:
        with_func_patcher:
            with_func_patcher:
                ...

    мы пишем
        with MultiFuncCallPatcher(*func_patchers):
            ...
    """
    def __init__(self, *func_call_patchers: FuncCallPatcher):
        self.func_call_patchers = func_call_patchers

    def __enter__(self):
        for func_call_patcher in self.func_call_patchers:
            func_call_patcher.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        for func_call_patcher in self.func_call_patchers:
            func_call_patcher.__exit__(*args, **kwargs)
