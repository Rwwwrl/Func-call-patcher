from func_call_patcher import FuncCallPatcher


def decorator_inner_func(func, func_args, func_kwargs, frame, relationship_identifier):
    return func(*func_args, **func_kwargs)


class TestFuncPatcher:
    def test_that_second_patcher_will_not_work(self, PACKAGE2_PATH):
        """
        тестируем, что второй патч на одну и ту же функцию не навесится
        """
        from func_call_patcher.pytests.playground.package2 import use_cases_X

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=11,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_cases_X.src1.some_func',
            executable_module_name='use_cases_X.py',
            line_number_where_func_executed=11,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.is_patched is True
                assert same_func_call_patcher._patcher.is_patched is False
                use_cases_X.Case_1.run()


class TestMethodPatcher:
    def test_that_second_patcher_on_method_will_not_work(self, PACKAGE2_PATH):
        """
        тестируем, что второй патч на один и тот же метод не навесится
        """
        from func_call_patcher.pytests.playground.package2 import use_casesX

        # use case 6
        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.RobotModel.get_passport_value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=73,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.RobotModel.get_passport_value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=73,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.is_patched is True
                assert same_func_call_patcher._patcher.is_patched is False
                use_casesX.Case6.run()

    def test_that_second_patcher_on_property_will_not_work(self, PACKAGE2_PATH):
        """
        тестируем, что второй патч на один и тот же метод не навесится
        """
        from func_call_patcher.pytests.playground.package2 import use_casesX

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Robot.value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=117,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.use_casesX.Robot.value',
            executable_module_name='use_casesX.py',
            line_number_where_func_executed=117,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.is_patched is True
                assert same_func_call_patcher._patcher.is_patched is False
                use_casesX.Case10.run()
