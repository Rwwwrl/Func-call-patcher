import os
from pathlib import Path
from types import FrameType

from func_call_patcher import FuncCallPatcher, MultiFuncCallPatcher

import pytest

EXPECTED_RESULTS = Path(__file__).absolute().parent / 'expected_results'
FILE_PATH = EXPECTED_RESULTS / 'file.txt'


def decorator_inner_func(
    func,
    func_args,
    func_kwargs,
    frame: FrameType,
    relationship_identifier,
):
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


class TestFuncCallPatcherCaseX:
    def test_case1(self, file_deleter, PACKAGE2_PATH):

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.some_func',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=20,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            from func_call_patcher.pytests.playground.package2 import use_casesX    # noqa
            assert_file_not_exists()

    def test_case2(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.some_func',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=30,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            use_casesX.Case2.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case2.run()
        assert_file_not_exists()

    def test_case3(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.some_func',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=39,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            use_casesX.Case3.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case3.run()
        assert_file_not_exists()

    def test_case4(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.some_func',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=53,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            use_casesX.Case4.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case4.run()
        assert_file_not_exists()

    def test_case5(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Agreggator.some_classmethod',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=64,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case5.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case5.run()
        assert_file_not_exists()

    def test_case6(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.RobotModel.get_passport_value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=73,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case6.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case6.run()
        assert_file_not_exists()

    def test_case7(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.RobotModel.get_passport_value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=82,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case7.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case7.run()
        assert_file_not_exists()

    def test_case8(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.local_func',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=91,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            use_casesX.Case8.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case8.run()
        assert_file_not_exists()

    def test_case9(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        path = f'{PACKAGE2_PATH}.use_casesX.Case9.SomeClass.src_func'
        func_call_patcher = FuncCallPatcher(
            path_to_func=path,
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=108,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case9.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case9.run()
        assert_file_not_exists()

    def test_case10(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Robot.value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=117,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case10.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case10.run()
        assert_file_not_exists()

    def test_case11(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src2.Dependency.some_property',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=126,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case11.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case11.run()
        assert_file_not_exists()

    def test_case12(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src2.Dependency.some_method',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=135,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case12.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case12.run()
        assert_file_not_exists()

    def test_case13(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Agreggator.some_statitcmethod',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=144,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case13.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case13.run()
        assert_file_not_exists()

    def test_case14(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Agreggator.some_method_with_decorator_on_it',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=153,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case14.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case14.run()
        assert_file_not_exists()

    def test_case15(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Agreggator.some_property_with_decorator_on_it',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=162,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case15.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case15.run()
        assert_file_not_exists()

    def test_case16(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.some_func_with_decorator_on_it',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=171,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            use_casesX.Case16.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case16.run()
        assert_file_not_exists()

    def test_case17(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src3.Dependency.some_property',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=180,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case17.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case17.run()
        assert_file_not_exists()

    def test_case18(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src1.some_func',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=191,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_casesX.Case18.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_casesX.Case18.run()
        assert_file_not_exists()


class TestFuncCallPatcherCase_X:
    def test_case_1(self, file_deleter, PACKAGE2_PATH):
        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=13,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            from func_call_patcher.pytests.playground.package2 import use_casesX    # noqa
            assert_file_not_exists()

    def test_case_2(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=23,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            use_cases_X.Case_2.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_2.run()
        assert_file_not_exists()

    def test_case_3(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=32,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            use_cases_X.Case_3.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_3.run()
        assert_file_not_exists()

    def test_case_4(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=46,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )

        with func_call_patcher:
            use_cases_X.Case_4.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_4.run()
        assert_file_not_exists()

    def test_case_5(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.Agreggator.some_classmethod',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=57,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_5.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_5.run()
        assert_file_not_exists()

    def test_case_6(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.RobotModel.get_passport_value',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=66,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_6.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_6.run()
        assert_file_not_exists()

    def test_case_7(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.RobotModel.get_passport_value',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=75,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_7.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_7.run()
        assert_file_not_exists()

    def test_case_8(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.local_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=84,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            use_cases_X.Case_8.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_8.run()
        assert_file_not_exists()

    def test_case_9(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        path = f'{PACKAGE2_PATH}.use_cases_X.Case_9.SomeClass.src_func'
        func_call_patcher = FuncCallPatcher(
            path_to_func=path,
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=101,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_9.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_9.run()
        assert_file_not_exists()

    def test_case_10(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.Robot.value',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=110,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_10.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_10.run()
        assert_file_not_exists()

    def test_case_11(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src2.Dependency.some_property',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=119,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_11.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_11.run()
        assert_file_not_exists()

    def test_case_12(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src2.Dependency.some_method',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=128,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_12.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_12.run()
        assert_file_not_exists()

    def test_case_13(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.Agreggator.some_statitcmethod',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=137,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_13.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_13.run()
        assert_file_not_exists()

    def test_case_14(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.Agreggator.some_method_with_decorator_on_it',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=146,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_14.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_14.run()
        assert_file_not_exists()

    def test_case_15(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.Agreggator.some_property_with_decorator_on_it',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=155,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_15.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_15.run()
        assert_file_not_exists()

    def test_case_16(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func_with_decorator_on_it',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=164,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            use_cases_X.Case_16.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_16.run()
        assert_file_not_exists()

    def test_case_17(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src3.Dependency.some_property',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=173,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_17.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_17.run()
        assert_file_not_exists()

    def test_case_18(self, file_deleter, PACKAGE1_PATH):
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE1_PATH}.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=184,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            use_cases_X.Case_18.run()
            assert_file_exists()

        # проверяем, что патч спадет после выхода из контекстного менеджера
        delete_file()
        use_cases_X.Case_18.run()
        assert_file_not_exists()


class TestMultiFuncCallPatcher:
    @staticmethod
    def decorator_inner_func(func, func_args, func_kwargs, *args):
        return func(*func_args, **func_kwargs)

    def test_patch(self, file_deleter, PACKAGE2_PATH):
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patchers = [
        # use case 4
            FuncCallPatcher(
                path_to_func=f'{PACKAGE2_PATH}.use_casesX.some_func',
                executable_module_name='use_casesX.py',
                line_number_where_func_executed=53,
                decorator_inner_func=decorator_inner_func,
                is_method=False,
            ),
        # use case 5
            FuncCallPatcher(
                path_to_func=f'{PACKAGE2_PATH}.use_casesX.Agreggator.some_classmethod',
                executable_module_name='use_casesX.py',
                line_number_where_func_executed=64,
                decorator_inner_func=decorator_inner_func,
                is_method=True,
            ),
        ]

        multi_func_call_patcher = MultiFuncCallPatcher(*func_call_patchers)
        with multi_func_call_patcher:
            use_casesX.Case4.run()
            assert_file_exists()
            delete_file()
            assert_file_not_exists()
            use_casesX.Case5.run()
            assert_file_exists()
