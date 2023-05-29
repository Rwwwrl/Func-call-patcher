from typing import Callable, Tuple, Type

from . import exceptions
from .utils import Path


class ImportTool:
    @staticmethod
    def _raise_it_cannot_be_imported_error(path_to_func_in_executable_module: Path):
        raise exceptions.ItCannotBeImported(f"это не может быть импортировано {path_to_func_in_executable_module.path}")

    @staticmethod
    def _import_class_and_method_from_string(path_to_func_in_executable_module: Path) -> Tuple[Type, Callable]:
        path_to_func_in_executable_module_splitted = path_to_func_in_executable_module.split('.')
        full_path_to_module = '.'.join(path_to_func_in_executable_module_splitted[:-3])
        module_name, class_name, method_name = path_to_func_in_executable_module_splitted[-3:]

        try:
            exec(f'from {full_path_to_module} import {class_name}')
        except Exception:
            exec(f'from {full_path_to_module} import {module_name}')
            module_name = locals()[module_name]
            class_obj = getattr(module_name, class_name)
        else:
            class_obj = locals()[class_name]
        method = getattr(class_obj, method_name)
        return class_obj, method

    @classmethod
    def import_class_and_method_from_string(cls, path_to_func_in_executable_module: Path) -> Tuple[Type, Callable]:
        try:
            return cls._import_class_and_method_from_string(
                path_to_func_in_executable_module=path_to_func_in_executable_module,
            )
        except Exception:
            cls._raise_it_cannot_be_imported_error(path_to_func_in_executable_module=path_to_func_in_executable_module)

    @classmethod
    def _import_func_from_string(cls, path_to_func_in_executable_module: Path) -> Callable:
        path_to_func_in_executable_module_splitted = path_to_func_in_executable_module.split('.')
        full_path_to_module = '.'.join(path_to_func_in_executable_module_splitted[:-2])
        module_name, func_name = path_to_func_in_executable_module_splitted[-2:]

        try:
            exec(f'from {full_path_to_module} import {func_name}')
        except Exception:
            exec(f'from {full_path_to_module} import {module_name}')
            module = locals()[module_name]
            func = getattr(module, func_name)
        else:
            func = locals()[func_name]

        return func

    @classmethod
    def import_func_from_string(cls, path_to_func_in_executable_module: Path) -> Callable:
        try:
            return cls._import_func_from_string(path_to_func_in_executable_module=path_to_func_in_executable_module)
        except Exception:
            cls._raise_it_cannot_be_imported_error(path_to_func_in_executable_module=path_to_func_in_executable_module)
