import os
from typing import List


class Path:
    def __init__(self, path: str, is_path_to_method: bool):
        self._path = path
        self._is_path_to_method = is_path_to_method

    @property
    def path(self) -> str:
        return self._path

    def split(self, sep: str) -> List:
        return self.path.split(sep=sep)

    @property
    def abc_path_to_executable_module(self) -> str:
        """
        возращает полный путь до запускаемого модуля где находится запатченная функция/метод

        Пример:
            playground.package2.service.some_func -> playground/package2/service.py
        """
        path_to_func = self.split('.')
        if self._is_path_to_method:
            path = path_to_func[:-2]
        else:
            path = path_to_func[:-1]
        return os.path.join(*path) + '.py'
