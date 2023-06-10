import abc
from typing import Any, List

from attrs import define

from .exceptions import ItCannotBeImported
from .import_tool import ImportTool


@define
class PathData:

    path_to_func: str
    is_method: bool


class BaseValidatationException(BaseException):
    pass


class LineNumberIsIncorrect(BaseValidatationException):
    pass


class ExecutableModuleNameIsIncorrect(BaseValidatationException):
    pass


class PathToFuncIsIncorrect(BaseValidatationException):
    pass


class IValidator(abc.ABC):
    def __init__(self, obj: Any):
        self.obj = obj

    @abc.abstractmethod
    def validate(self) -> None:
        raise NotImplementedError


class LineNumberValidator(IValidator):

    obj: int

    def validate(self) -> None:
        if self.obj <= 0:
            raise LineNumberIsIncorrect(f"{self.obj} должно > 0")


class ExecutableModuleNameValidator(IValidator):

    obj: str

    def validate(self) -> None:
        try:
            filename, file_ext = self.obj.split('.')
        except ValueError:
            raise ExecutableModuleNameIsIncorrect('формат имени модуля должен быть: <filename>.py')
        if not filename:
            raise ExecutableModuleNameIsIncorrect('наименование файла не должно быть пустым')
        if file_ext != '.py':
            raise ExecutableModuleNameIsIncorrect('расширение файла должно быть ".py"')


class FuncCanBeImportedValidator(IValidator):

    obj: PathData

    def validate(self) -> None:
        if self.obj.is_method:
            import_func = ImportTool.import_class_and_method_from_string
        else:
            import_func = ImportTool.import_func_from_string

        try:
            import_func(path_to_func=self.obj.path_to_func)
        except ItCannotBeImported:
            if self.obj.is_method:
                func_type = 'метод'
                declension = 'импортирован'
            else:
                func_type = 'функция'
                declension = 'импортированa'
            raise PathToFuncIsIncorrect(
                f"""
                {func_type} по пути '{self.obj.path_to_func.path}' не может быть {declension},
                проверьте правильно ли вы указали путь.
                """,
            )


def validate(
    line_number_where_func_executed: int,
    executable_module_name: str,
    path_to_func: str,
    is_method: bool,
):
    validators: List[IValidator] = [
        LineNumberValidator(obj=line_number_where_func_executed),
        FuncCanBeImportedValidator(obj=PathData(
            path_to_func=path_to_func,
            is_method=is_method,
        )),
        ExecutableModuleNameValidator(obj=executable_module_name),
    ]

    for validator in validators:
        validator.validate()
