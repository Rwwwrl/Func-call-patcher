import abc
import os
import sys
from typing import Callable, Optional

from mock import Mock, patch

from . import hints
from .import_tool import ImportTool
from .utils import Path


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

        return inner

    def __enter__(self, *args, **kwargs):
        raise NotImplementedError

    def __exit__(self, *args, **kwargs):
        raise NotImplementedError


class FuncPatcher(BasePatcher):
    def __enter__(self, *args, **kwargs):
        func_to_patch = ImportTool.import_func_from_string(
            path_to_func_in_executable_module=self.path_to_func_in_executable_module,
        )
        # TODO надо расписать объяснение на этот _does_func_need_a_patch
        self._does_func_need_a_patch = True
        if isinstance(func_to_patch, Mock) and hasattr(func_to_patch, '_is_from_func_patcher'):
            self._does_func_need_a_patch = False
            return self
        mock = Mock()
        mock._is_from_func_patcher = True
        mock.side_effect = self._decorate_func_call(func=func_to_patch)

        self._patcher = patch(self.path_to_func_in_executable_module.path, mock)
        self._patcher.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        if not self._does_func_need_a_patch:
            return
        self._patcher.__exit__(*args, **kwargs)
        del self._patcher


class MethodPatcher(BasePatcher):
    def __enter__(self, *args, **kwargs):
        class_obj, method = ImportTool.import_class_and_method_from_string(
            path_to_func_in_executable_module=self.path_to_func_in_executable_module,
        )

        self._original_method = method
        self._class_obj = class_obj
        setattr(self._class_obj, self._original_method.__name__, self._decorate_func_call(func=method))

    def __exit__(self, *args, **kwargs):
        setattr(self._class_obj, self._original_method.__name__, self._original_method)
        del self._original_method
        del self._class_obj
