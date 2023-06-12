from func_call_patcher import FuncCallPatcher, validators

from mock import Mock, patch

import pytest


def decorator_inner_func(func, func_args, func_kwargs, frame, relationship_identifier):
    return func(*func_args, **func_kwargs)


class TestIsFuncAlreadyPatchedValidator:
    def test_validate(self, PACKAGE2_PATH):
        path_to_func = f'{PACKAGE2_PATH}.use_casesX.some_func'
        executable_module_name = 'use_casesX.py'
        line_number_where_func_executed = 30
        is_method = False

        func_call_patcher = FuncCallPatcher(
            path_to_func=path_to_func,
            executable_module_name=executable_module_name,
            line_number_where_func_executed=line_number_where_func_executed,
            decorator_inner_func=decorator_inner_func,
            is_method=is_method,
        )

        path_data = validators.PathData(
            path_to_func=path_to_func,
            is_method=is_method,
        )

        with func_call_patcher:
            with pytest.raises(validators.FuncAlreadyPatched):
                validators.IsFuncAlreadyPatchedValidator(obj=path_data).validate()


class TestValidate:
    @patch.object(validators.IsFuncAlreadyPatchedValidator, 'validate')
    @patch.object(validators.IsFuncAlreadyPatchedValidator, '__init__')
    @patch.object(validators.ExecutableModuleNameValidator, 'validate')
    @patch.object(validators.ExecutableModuleNameValidator, '__init__')
    @patch.object(validators.FuncCanBeImportedValidator, 'validate')
    @patch.object(validators.FuncCanBeImportedValidator, '__init__')
    @patch.object(validators.LineNumberValidator, 'validate')
    @patch.object(validators.LineNumberValidator, '__init__')
    def test_validate(
        self,
        mock_line_number_validator___init__: Mock,
        mock_line_number_validator_validate: Mock,
        mock_func_can_be_imported_validator___init__: Mock,
        mock_func_can_be_imported_validate: Mock,
        mock_executable_module_name_validator___init__: Mock,
        mock_executable_module_name_validate: Mock,
        mock_is_func_already_patcher_validator___init__: Mock,
        mock_is_func_already_patcher_validator_validate: Mock,
    ):
        mock_line_number_validator___init__.return_value = None
        mock_func_can_be_imported_validator___init__.return_value = None
        mock_executable_module_name_validator___init__.return_value = None
        mock_is_func_already_patcher_validator___init__.return_value = None

        path_to_func = 'path_to_func'
        executable_module_name = 'executable_module_name'
        line_number_where_func_executed = 30
        is_method = False

        path_data = validators.PathData(path_to_func=path_to_func, is_method=is_method)

        validators.validate(
            line_number_where_func_executed=line_number_where_func_executed,
            executable_module_name=executable_module_name,
            path_to_func=path_to_func,
            is_method=is_method,
        )

        mock_line_number_validator___init__.assert_called_once_with(obj=line_number_where_func_executed)
        mock_func_can_be_imported_validator___init__.assert_called_once_with(obj=path_data)
        mock_executable_module_name_validator___init__.assert_called_once_with(obj=executable_module_name)
        mock_is_func_already_patcher_validator___init__.assert_called_once_with(obj=path_data)

        mock_line_number_validator_validate.assert_called_once()
        mock_func_can_be_imported_validate.assert_called_once()
        mock_executable_module_name_validate.assert_called_once()
        mock_is_func_already_patcher_validator_validate.assert_called_once()
