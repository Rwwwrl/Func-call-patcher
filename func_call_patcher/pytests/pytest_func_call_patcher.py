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
    def test_case0(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import second_service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.second_service.logic.some_func',
            executable_module_name='second_service.py',
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

    def test_case1(self, file_deleter, PACKAGE2_PATH):

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.some_func',
            executable_module_name='service.py',
            line_number_where_func_executed=6,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            from func_call_patcher.pytests.playground.package2 import service    # noqa
            assert_file_not_exists()

    def test_case2(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.some_func',
            executable_module_name='service.py',
            line_number_where_func_executed=20,
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

    def test_case3(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.some_func',
            executable_module_name='service.py',
            line_number_where_func_executed=28,
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

    def test_case4(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.some_func',
            executable_module_name='service.py',
            line_number_where_func_executed=36,
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

    def test_case5(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.Agreggator.some_classmethod',
            executable_module_name='service.py',
            line_number_where_func_executed=45,
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

    def test_case6(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.RobotModel.get_passport_value',
            executable_module_name='service.py',
            line_number_where_func_executed=56,
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

    def test_case7(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.RobotModel.get_passport_value',
            executable_module_name='service.py',
            line_number_where_func_executed=63,
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

    def test_case8(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.func_to_patch_in_executed_module',
            executable_module_name='service.py',
            line_number_where_func_executed=74,
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

    def test_case9(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        path = f'{PACKAGE2_PATH}.service.SomeClass.func_to_patch_in_executed_module'
        func_call_patcher = FuncCallPatcher(
            path_to_func=path,
            executable_module_name='service.py',
            line_number_where_func_executed=86,
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

    def test_case10(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        path = f'{PACKAGE2_PATH}.service.Robot.value'
        func_call_patcher = FuncCallPatcher(
            path_to_func=path,
            executable_module_name='service.py',
            line_number_where_func_executed=93,
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

    def test_case11(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.second_logic.Dependency.some_property',
            executable_module_name='service.py',
            line_number_where_func_executed=100,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.case11()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case11()
        assert_file_not_exists()

    def test_case12(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.second_logic.Dependency.some_method',
            executable_module_name='service.py',
            line_number_where_func_executed=107,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.case12()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case12()
        assert_file_not_exists()

    def test_case13(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.Agreggator.some_statitcmethod',
            executable_module_name='service.py',
            line_number_where_func_executed=114,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.case13()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case13()
        assert_file_not_exists()

    def test_case14(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.Agreggator.some_method_with_decorator_on_it',
            executable_module_name='service.py',
            line_number_where_func_executed=121,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.case14()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case14()
        assert_file_not_exists()

    def test_case15(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.Agreggator.some_property_with_decorator_on_it',
            executable_module_name='service.py',
            line_number_where_func_executed=128,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            service.case15()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case15()
        assert_file_not_exists()

    def test_case16(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.some_func_with_decorator_on_it',
            executable_module_name='service.py',
            line_number_where_func_executed=135,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            service.case16()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        service.case16()
        assert_file_not_exists()


class TestMultiFuncCallPatcher:
    @staticmethod
    def decorator_inner_func(func, func_args, func_kwargs, *args):
        return func(*func_args, **func_kwargs)

    def test_patch(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patchers = [
            FuncCallPatcher(
                path_to_func=f'{PACKAGE2_PATH}.service.some_func',
                executable_module_name='service.py',
                line_number_where_func_executed=36,
                decorator_inner_func=decorator_inner_func,
                is_method=False,
            ),
            FuncCallPatcher(
                path_to_func=f'{PACKAGE2_PATH}.service.Agreggator.some_classmethod',
                executable_module_name='service.py',
                line_number_where_func_executed=45,
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
