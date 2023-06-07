import pytest


@pytest.fixture(scope='session')
def PLAYGROUND_PATH_PREFIX() -> str:
    return 'func_call_patcher.pytests.playground.package2'
