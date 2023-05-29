import os
from pathlib import Path
from types import FrameType

from func_call_patcher import FuncCallPatcher, MultiFuncCallPatcher

import pytest

EXPECTED_RESULTS = Path(__file__).absolute().parent / 'expected_results'
FILE_PATH = EXPECTED_RESULTS / 'file.txt'


def decorator_inner_func(func, func_args, func_kwargs, frame: FrameType):
    with open(FILE_PATH, 'w'):
        return func(*func_args, **func_kwargs)


def assert_file_exists():
    assert FILE_PATH.exists() is True


def assert_file_not_exists():
    assert FILE_PATH.exists() is False


@pytest.fixture()
def playground_path_prefix() -> str:
    return 'func_call_patcher.pytests.playground.package2'


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


class TestFuncPathcher:
    def test_inside_func_with_import_func_from_module(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.some_func',
            line_number_where_func_executed=11,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            service.service_func()
            assert_file_exists()

    def test_inside_func_with_import_module_from_package(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import second_service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.second_service.logic.some_func',
            line_number_where_func_executed=8,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            second_service.service_func()
            assert_file_exists()

    def test_inside_global_scope(self, file_deleter, playground_path_prefix):

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.some_func',
            line_number_where_func_executed=4,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            from func_call_patcher.pytests.playground.package2 import service    # noqa
            assert_file_not_exists()

    def test_inside_method(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.some_func',
            line_number_where_func_executed=18,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            service.Some()
            assert_file_exists()

    def test_inside_many_scopes(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.some_func',
            line_number_where_func_executed=25,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            service.another_service_func()()
            assert_file_exists()

    def test_patch_classmethod(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.Agreggator.execute',
            line_number_where_func_executed=33,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.classmethod_execute()
            assert_file_exists()

    def test_patch_instancemethod(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.RobotModel.get_passport_value',
            line_number_where_func_executed=43,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.instancemethod_execute()
            assert_file_exists()

    def test_patch_inner_instancemethod(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{playground_path_prefix}.service.RobotModel.get_passport_value',
            line_number_where_func_executed=49,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.instancemethod_execute2()
            assert_file_exists()


class TestMultiFuncCallPatcher:
    @staticmethod
    def decorator_inner_func(func, func_args, func_kwargs, *args):
        return func(*func_args, **func_kwargs)

    def test_patch(self, file_deleter, playground_path_prefix):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patchers = [
            FuncCallPatcher(
                path_to_func_in_executable_module=f'{playground_path_prefix}.service.some_func',
                line_number_where_func_executed=25,
                decorator_inner_func=decorator_inner_func,
                is_method=False,
            ),
            FuncCallPatcher(
                path_to_func_in_executable_module=f'{playground_path_prefix}.service.Agreggator.execute',
                line_number_where_func_executed=33,
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
