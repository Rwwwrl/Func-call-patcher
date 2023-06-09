from func_call_patcher import FuncCallPatcher


def decorator_inner_func(func, func_args, func_kwargs, frame, relationship_identifier):
    return func(*func_args, **func_kwargs)


class TestFuncPatcher:
    def test_that_second_patcher_will_not_work(self, PLAYGROUND_PATH_PREFIX):
        """
        тестируем, что второй патч на одну и ту же функцию не навесится
        """
        from func_call_patcher.pytests.playground.package2 import second_service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.second_service.logic.some_func',
            line_number_where_func_executed=9,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.second_service.logic.some_func',
            line_number_where_func_executed=9,
            decorator_inner_func=decorator_inner_func,
            is_method=False,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.data_container.does_func_need_a_patch is True
                assert same_func_call_patcher._patcher.data_container.does_func_need_a_patch is False
                second_service.service_func()


class TestMethodPatcher:
    def test_that_second_patcher_on_method_will_not_work(self, PLAYGROUND_PATH_PREFIX):
        """
        тестируем, что второй патч на один и тот же метод не навесится
        """
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.RobotModel.get_passport_value',
            line_number_where_func_executed=49,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.RobotModel.get_passport_value',
            line_number_where_func_executed=49,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.data_container.does_method_need_a_patch is True
                assert same_func_call_patcher._patcher.data_container.does_method_need_a_patch is False
                service.instancemethod_execute()

    def test_that_second_patcher_on_property_will_not_work(self, PLAYGROUND_PATH_PREFIX):
        """
        тестируем, что второй патч на один и тот же метод не навесится
        """
        from func_call_patcher.pytests.playground.package2 import service

        func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.Robot.value',
            line_number_where_func_executed=86,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        same_func_call_patcher = FuncCallPatcher(
            path_to_func_in_executable_module=f'{PLAYGROUND_PATH_PREFIX}.service.Robot.value',
            line_number_where_func_executed=86,
            decorator_inner_func=decorator_inner_func,
            is_method=True,
        )
        with func_call_patcher:
            with same_func_call_patcher:
                assert func_call_patcher._patcher.data_container.does_method_need_a_patch is True
                assert same_func_call_patcher._patcher.data_container.does_method_need_a_patch is False
                service.instancemethod_execute()
