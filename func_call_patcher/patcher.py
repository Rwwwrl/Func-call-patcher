import abc
import functools
import os
import sys
from typing import Callable, Optional

from mock import Mock, patch

from . import hints
from .import_tool import ImportTool
from .utils import Path

PATCHED_BY_FUNC_CALL_PATCHER_TAG = '_patched_by_func_call_patcher'


def compare_paths(frame_path: str, abc_path_to_executable_module: str) -> bool:
    """
    функция отвечает на вопрос, является ли abc_path_to_module частью пути frame_path

    Пример 1:
        path1 = "/patch_funcs/func_call_patcher/playground/package2/second_service.py"
        path2 = "playground/package2/second_service/logic.py"
        являтся одними и теми же путями, просто в случае path2 мы делаем импорт вида
             # second_service.py
             from package import logic

             logic.some_func()

        compare_paths(path1, path2) -> True

    Пример 2:
        path1 = "/patch_funcs/func_call_patcher/playground/package2/second_service.py"
        path2 = "playground/package2/second_service.py"
        тут очиведно почему пути являются одними и теми же. В этом случае импорт выглядит как
             # second_service.py
             from package.logic import some_func

             some_func()
    """
    # TODO скорее всего эту логику тем или иным образом надо внести в utils.Path

    if frame_path.endswith(abc_path_to_executable_module):
        return True

    # если до сюда дошли, значит импорт выглядит как примере 1. Убираем из abc_path_to_module импортирумый модуль.
    splitted_abc_path = abc_path_to_executable_module.split(os.sep)
    abc_path_to_executable_module = os.sep.join(splitted_abc_path[:-1]) + '.py'
    return frame_path.endswith(abc_path_to_executable_module)


class DataContainer:
    """нужен для переноса данных между __enter__ и __exit__, которые не хотелось бы хранить в self"""
    pass


class IPatcher(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        path_to_func_in_executable_module: Path,
        line_where_func_executed: int,
        decorator_inner_func: hints.DecoratorInnerFunc,
        relationship_identifier: Optional[hints.RelationshipIdentifier] = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def __enter__(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args, **kwargs):
        raise NotImplementedError


class BasePatcher(IPatcher):
    def __init__(
        self,
        path_to_func_in_executable_module: Path,
        line_number_where_func_executed: int,
        decorator_inner_func: hints.DecoratorInnerFunc,
        relationship_identifier: Optional[hints.RelationshipIdentifier] = None,
    ):
        self.path_to_func_in_executable_module = path_to_func_in_executable_module
        self.decorator_inner_func = decorator_inner_func
        self.line_where_func_executed = line_number_where_func_executed
        self.relationship_identifier = relationship_identifier

    def _decorate_func_call(self, func: Callable):
        abc_path_to_executable_module = self.path_to_func_in_executable_module.abc_path_to_executable_module

        @functools.wraps(func)
        def inner(*args, **kwargs):
            frame = sys._getframe()
            while frame.f_back:
                full_path_of_module_in_executed_frame = frame.f_code.co_filename
                if (
                    frame.f_lineno == self.line_where_func_executed and    # noqa
                    compare_paths(
                        frame_path=full_path_of_module_in_executed_frame,
                        abc_path_to_executable_module=abc_path_to_executable_module,
                    )
                ):
                    result = self.decorator_inner_func(func, args, kwargs, frame, self.relationship_identifier)
                    return result
                frame = frame.f_back
            return func(*args, **kwargs)

        # помечаем функцию внутреннюю функцию как функция из func_call_patcher
        # это нужно для MethodPatcher._is_method_aready_patched
        setattr(inner, PATCHED_BY_FUNC_CALL_PATCHER_TAG, True)
        return inner

    def __enter__(self, *args, **kwargs):
        raise NotImplementedError

    def __exit__(self, *args, **kwargs):
        raise NotImplementedError


class FuncPatcher(BasePatcher):
    def _is_func_already_patched(self, func) -> bool:
        return isinstance(func, Mock) and hasattr(func, PATCHED_BY_FUNC_CALL_PATCHER_TAG)

    def __enter__(self, *args, **kwargs):
        func_to_patch = ImportTool.import_func_from_string(
            path_to_func_in_executable_module=self.path_to_func_in_executable_module,
        )
        self.data_container = DataContainer()

        if self._is_func_already_patched(func=func_to_patch):
            self.data_container.does_func_need_a_patch = False
            return self
        self.data_container.does_func_need_a_patch = True
        mock = Mock()
        setattr(mock, PATCHED_BY_FUNC_CALL_PATCHER_TAG, True)
        mock.side_effect = self._decorate_func_call(func=func_to_patch)

        self.data_container.patcher = patch(self.path_to_func_in_executable_module.path, mock)
        self.data_container.patcher.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        if not self.data_container.does_func_need_a_patch:
            return
        self.data_container.patcher.__exit__(*args, **kwargs)


class MethodPatcher(BasePatcher):
    def _is_method_aready_patched(self, method) -> bool:
        return hasattr(method, PATCHED_BY_FUNC_CALL_PATCHER_TAG)

    def _is_property_already_patched(self, method) -> bool:
        return hasattr(method.fget, PATCHED_BY_FUNC_CALL_PATCHER_TAG)

    def __enter__(self, *args, **kwargs):
        class_obj, method = ImportTool.import_class_and_method_from_string(
            path_to_func_in_executable_module=self.path_to_func_in_executable_module,
        )
        self.data_container = DataContainer()
        # TODO это разветвление нужно вынести
        if isinstance(method, property):
            if self._is_property_already_patched(method=method):
                self.data_container.does_method_need_a_patch = False
                return self

            self.data_container.is_property = True
            patched_property = property(
                fget=self._decorate_func_call(func=method.fget),
                fset=method.fset,
                fdel=method.fdel,
            )
            setattr(class_obj, method.fget.__name__, patched_property)
            self.data_container.original_property = method

        else:
            if self._is_method_aready_patched(method=method):
                self.data_container.does_method_need_a_patch = False
                return self

            self.data_container.is_method = True
            setattr(class_obj, method.__name__, self._decorate_func_call(func=method))
            self.data_container.original_method = method

        self.data_container.does_method_need_a_patch = True
        self.data_container.class_obj = class_obj

    def __exit__(self, *args, **kwargs):
        if not self.data_container.does_method_need_a_patch:
            return

        if hasattr(self.data_container, 'is_property'):
            setattr(
                self.data_container.class_obj,
                self.data_container.original_property.fget.__name__,
                self.data_container.original_property,
            )
            return
        elif hasattr(self.data_container, 'is_method'):
            setattr(
                self.data_container.class_obj,
                self.data_container.original_method.__name__,
                self.data_container.original_method,
            )
            return
