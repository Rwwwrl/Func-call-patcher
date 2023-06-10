# func-patcher

Задачей данного FuncPatcher`а является запатчить один конкретный вызов функции/метода в _запускаемом_ модуле.

_запускаемый_ модуль - модуль, в котором запускается функция/метод, которую мы хотим пропатчить

Пример:

Пусть у нас есть такая структура проекта

```bash ├── package1
│   └── logic.py
├── package2
│   └── service.py
└── run.py
```

содержимое файлов

**logic\.py**

```python
# logic.py
def some_func(x=None) -> int:
    return 10
```

**service\.py**

```python
from package1.logic import some_func


def service_func():
    return some_func(x=10)  # номер строки = 5
```

**run\.py**

```python
from package2 import service

result = service.service_func()
```

Мы запускаем _run\.py_, который импортирует _package2.service_, который в свою очередь импортирует _package1.logic_.
Мы бы хотели пропатчить вызов функции _some_func_ внутри модуля _service.py_, а именно вызов на 5 строчке. Для простоты, функция, которой мы будем патчить будет просто выводить аргументы, с которыми вызовется _some_func_, в консоль.

Тогда патч в нашем случае выглядит:

**run\.py**

```python
# run.py
from package2 import service

from func_call_patcher import FuncCallPatcher


def decorator_inner_func(func, func_args, func_kwargs, frame, relationship_identifier):
    print(f'func_args = {func_args}, func_kwargs = {func_kwargs}')
    return func(*func_args, **func_kwargs)


func_call_patcher = FuncCallPatcher(
    path_to_func='package2.service.some_func',
    line_number_where_func_executed=5,
    executable_module_name='service.py',
    decorator_inner_func=decorator_inner_func,
    is_method=False,
)

with func_call_patcher:
    result = service.service_func()
```

Теперь при запуске _run.py_ мы увидим принт `func_args = (), func_kwargs = {'x': 10}`

Больше примеров можно найти в _func_call_patcher/pytests/pytest_func_patcher\.py_
