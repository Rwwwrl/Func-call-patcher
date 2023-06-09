import os
from pathlib import Path
from types import FrameType

from func_call_patcher import FuncCallPatcher, MultiFuncCallPatcher

import pytest

EXPECTED_RESULTS = Path(__file__).absolute().parent / 'expected_results'
FILE_PATH = EXPECTED_RESULTS / 'file.txt'


def decorator_inner_func(func, func_args, func_kwargs, frame: FrameType, relationship_identifier):
    with open(FILE_PATH, 'w'):
        return func(*func_args, **func_kwargs)


def assert_file_exists():
    assert FILE_PATH.exists() is True


def assert_file_not_exists():
    assert FILE_PATH.exists() is False


def delete_file():
    try:
        os.remove(FILE_PATH)
    except FileNotFoundError:
        pass


@pytest.fixture()
def file_deleter():
    yield
    # teardown
    delete_file()


class TestFuncCallPatcher:
    def test_case0(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import second_service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.second_service.logic.some_func',
            line_number_where_func_executed=9,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            second_service.service_func()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        second_service.service_func()
        assert_file_not_exists()

    def test_case1(self, file_deleter, PLAYGROUND_PATH_PREFIX):

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.some_func',
            line_number_where_func_executed=5,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            from func_call_patcher.pytests.playground.package2 import service    # noqa
            assert_file_not_exists()

    def test_case2(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.some_func',
            line_number_where_func_executed=13,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            service.service_func()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.service_func()
        assert_file_not_exists()

    def test_case3(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.some_func',
            line_number_where_func_executed=21,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            service.Some()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.Some()
        assert_file_not_exists()

    def test_case4(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.some_func',
            line_number_where_func_executed=29,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            service.another_service_func()()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.another_service_func()()
        assert_file_not_exists()

    def test_case5(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.Agreggator.execute',
            line_number_where_func_executed=38,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.classmethod_execute()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.classmethod_execute()
        assert_file_not_exists()

    def test_case6(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.RobotModel.get_passport_value',
            line_number_where_func_executed=49,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.instancemethod_execute()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.instancemethod_execute()
        assert_file_not_exists()

    def test_case7(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.RobotModel.get_passport_value',
            line_number_where_func_executed=56,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.instancemethod_execute2()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.instancemethod_execute2()
        assert_file_not_exists()

    def test_case8(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.func_to_patch_in_executed_module',
            line_number_where_func_executed=67,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            service.outer_func_to_patch_in_executed_module()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.outer_func_to_patch_in_executed_module()
        assert_file_not_exists()

    def test_case9(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        path = f'{PLAYGROUND_PATH_PREFIX}.service.SomeClass.func_to_patch_in_executed_module'
        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=path,
            line_number_where_func_executed=79,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.SomeClass().outer_func_to_patch_in_executed_module()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.SomeClass().outer_func_to_patch_in_executed_module()
        assert_file_not_exists()

    def test_case10(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        path = f'{PLAYGROUND_PATH_PREFIX}.service.Robot.value'
        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=path,
            line_number_where_func_executed=86,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.case10()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case10()
        assert_file_not_exists()


class TestMultiFuncCallPatcher:
    @staticmethod
    def decorator_inner_func(func, func_args, func_kwargs, *args):
        return func(*func_args, **func_kwargs)

    def test_patch(self, file_deleter, PLAYGROUND_PATH_PREFIX):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patchers = [
            FuncCallPatcher(
                path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.some_func',
                line_number_where_func_executed=29,
                decorator_inner_func=decorator_inner_func,
                is_method=False,
            ),
            FuncCallPatcher(
                path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.Agreggator.execute',
                line_number_where_func_executed=38,
                decorator_inner_func=decorator_inner_func,
                is_method=True,
            ),
        ]

        multi_func_call_patcher = MultiFuncCallPatcher(*func_call_patchers)
        with multi_func_call_patcher:
            service.another_service_func()()
            assert_file_exists()
            delete_file()
            assert_file_not_exists()
            service.classmethod_execute()
            assert_file_exists()
