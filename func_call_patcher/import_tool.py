from typing import Callable, Tuple, Type

from . import exceptions


class ImportTool:
    @staticmethod
    def _raise_it_cannot_be_imported_error(path_to_func: str):
        raise exceptions.ItCannotBeImported(f"это не может быть импортировано {path_to_func}")

    @staticmethod
    def _import_class_and_method_from_string(path_to_func: str) -> Tuple[Type, Callable]:
        path_to_method_splitted = path_to_func.split('.')
        full_path_to_module = '.'.join(path_to_method_splitted[:-3])
        module_name, class_name, method_name = path_to_method_splitted[-3:]

        exec(f'from {full_path_to_module} import {module_name}')
        module_name = locals()[module_name]
        class_obj = getattr(module_name, class_name)
        method = getattr(class_obj, method_name)

        return class_obj, method

    @classmethod
    def import_class_and_method_from_string(cls, path_to_func: str) -> Tuple[Type, Callable]:
        try:
            return cls._import_class_and_method_from_string(path_to_func=path_to_func)
        except Exception:
            cls._raise_it_cannot_be_imported_error(path_to_func=path_to_func)

    @classmethod
    def _import_func_from_string(cls, path_fo_func: str) -> Callable:
        path_to_func_splitted = path_fo_func.split('.')
        full_path_to_module = '.'.join(path_to_func_splitted[:-2])
        module_name, func_name = path_to_func_splitted[-2:]

        exec(f'from {full_path_to_module} import {module_name}')
        module = locals()[module_name]
        func = getattr(module, func_name)

        return func

    @classmethod
    def import_func_from_string(cls, path_to_func: str) -> Callable:
        try:
            return cls._import_func_from_string(path_fo_func=path_to_func)
        except Exception:
            cls._raise_it_cannot_be_imported_error(path_to_func=path_to_func)
