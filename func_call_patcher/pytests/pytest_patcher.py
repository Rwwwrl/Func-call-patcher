from func_call_patcher import FuncCallPatcher


def decorator_inner_func(func, func_args, func_kwargs, frame, relationship_identifier):
    return func(*func_args, **func_kwargs)


class TestFuncPatcher:
    def test_that_second_patcher_will_not_work(self, PACKAGE2_PATH):
        """
        тестируем, что второй патч на одну и ту же функцию не навесится
        """
        from func_call_patcher.pytests.playground.package2 import second_service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.second_service.logic.some_func',
            executable_module_name='second_service.py',
            line_number_where_func_executed=15,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.second_service.logic.some_func',
            executable_module_name='second_service.py',
            line_number_where_func_executed=15,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.is_patched is True
                assert same_func_call_patcher._patcher.is_patched is False
                second_service.case_1()


class TestMethodPatcher:
    def test_that_second_patcher_on_method_will_not_work(self, PACKAGE2_PATH):
        """
        тестируем, что второй патч на один и тот же метод не навесится
        """
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.RobotModel.get_passport_value',
            executable_module_name='service.py',
            line_number_where_func_executed=55,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.RobotModel.get_passport_value',
            executable_module_name='service.py',
            line_number_where_func_executed=55,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.is_patched is True
                assert same_func_call_patcher._patcher.is_patched is False
                service.instancemethod_execute()

    def test_that_second_patcher_on_property_will_not_work(self, PACKAGE2_PATH):
        """
        тестируем, что второй патч на один и тот же метод не навесится
        """
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.Robot.value',
            executable_module_name='service.py',
            line_number_where_func_executed=92,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func=f'{PACKAGE2_PATH}.service.Robot.value',
            executable_module_name='service.py',
            line_number_where_func_executed=92,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.is_patched is True
                assert same_func_call_patcher._patcher.is_patched is False
                service.instancemethod_execute()
