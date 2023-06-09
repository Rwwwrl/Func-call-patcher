import pytest


@pytest.fixture(scope='session')
def PACKAGE2_PATH() -> str:
    return 'func_call_patcher.pytests.playground.package2'


@pytest.fixture(scope='session')
def PACKAGE1_PATH() -> str:
    return 'func_call_patcher.pytests.playground.package1'
