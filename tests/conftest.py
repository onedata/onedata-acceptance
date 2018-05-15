"""
Definitions of fixtures used in env_up, acceptance and performance tests.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests import *
from tests.utils.path_utils import (make_logdir, get_file_name, get_json_files,
                                    absolute_path_to_env_file)


import json
import pytest


def pytest_addoption(parser):
    parser.addoption("--test-type", action="store", default="acceptance",
                     help="type of test (acceptance, env_up,"
                          "performance, packaging, gui)")
    parser.addoption("--ignore-xfail", action="store_true",
                     help="Ignores xfail mark")
    parser.addoption("--env-file", action="store", default=None,
                     help="description of environment that will be tested")


def pytest_generate_tests(metafunc):
    if metafunc.config.option.test_type:
        test_type = metafunc.config.option.test_type
        if test_type == ['gui', 'mixed_swaggers'] and not metafunc.config.option.base_url:
            envs = get_json_files(map_test_type_to_env_dir(test_type),
                                  relative=True)
            metafunc.parametrize('env_description_file', envs, scope='module')

        elif test_type in ['acceptance', 'performance']:
            env_file = metafunc.config.getoption("env_file")
            if env_file:
                metafunc.parametrize('env_description_file', [env_file],
                                     scope='module')
            else:
                with open(map_test_type_to_test_config_file(test_type), 'r') as f:
                    test_config = json.load(f)

                test_file = metafunc.module.__name__.split('.')[-1]
                if test_file in test_config:
                    metafunc.parametrize(
                        'env_description_file',
                        [env_file for env_file in test_config[test_file]],
                        scope='module'
                    )

@pytest.fixture()
def skip_by_env(request, env_description_file):
    """This function skips test cases decorated with:
    @pytest.mark.skip_env(*envs).
    Test won't start for each env in envs.
    If you want to skip whole module, you must define
    global variable in that module named pytestmark in
    the following way:
    pytestmark = pytest.mark.skip_env(*envs)
    """
    if request.node.get_marker('skip_env'):
        env = get_file_name(env_description_file)
        args = request.node.get_marker('skip_env').kwargs
        reason = args['reason']
        arg_envs = [get_file_name(e) for e in args['envs']]
        if env in arg_envs:
            pytest.skip('skipped on env: {env} with reason: {reason}'
                        .format(env=env, reason=reason))


@pytest.fixture()
def xfail_by_env(request, env_description_file):
    """This function marks test cases decorated with:
    @pytest.mark.skip_env(*envs)
    as expected to fail:
    Test will be marked as expected to fail for each
    env in envs.
    If you want to mark whole module, you must define
    global variable in that module named pytestmark in
    the following way:
    pytestmark = pytest.mark.xfail_env(*envs)
    Running tests with --ignore-xfail causes xfail marks to be ignored.
    """
    if request.node.get_marker('xfail_env'):
        env = get_file_name(env_description_file)
        args = request.node.get_marker('xfail_env').kwargs
        reason = args['reason']
        arg_envs = [get_file_name(e) for e in args['envs']]
        ignore = request.config.getoption("--ignore-xfail")
        if env in arg_envs and not ignore:
            request.node.add_marker(pytest.mark.xfail(
                reason='xfailed on env: {env} with reason: {reason}'
                    .format(env=env, reason=reason)))


def map_test_type_to_env_dir(test_type):
    return {
        'acceptance': ACCEPTANCE_ENV_DIR,
        'performance': PERFORMANCE_ENV_DIR,
        'gui': GUI_ENV_DIR
    }[test_type]


def map_test_type_to_logdir(test_type):
    return {
        'acceptance': ACCEPTANCE_LOGDIR,
        'performance': PERFORMANCE_LOGDIR,
        'mixed_swaggers': MIXED_SWAGGERS_LOGDIR,
        'gui': GUI_LOGDIR
    }.get(test_type, ACCEPTANCE_LOGDIR)


def map_test_type_to_test_config_file(test_type):
    return {
        'acceptance': ACCEPTANCE_TEST_CONFIG,
        'performance': PERFORMANCE_TEST_CONFIG
    }.get(test_type, ACCEPTANCE_LOGDIR)


def get_test_type(request):
    return request.config.getoption("test_type")

