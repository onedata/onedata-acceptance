"""
Definitions of fixtures used in acceptance tests.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
import re
import yaml
import pytest

from tests import (ENV_DIRS, SCENARIO_DIRS, PATCHES_DIR, ENTITIES_CONFIG_DIR, LOGDIRS)
from tests.utils import CLIENT_POD_LOGS_DIR
from tests.utils.user_utils import AdminUser
from tests.utils.environment_utils import start_environment, clean_env
from tests.utils.path_utils import (get_file_name, absolute_path_to_env_file,
                                    make_logdir)
from tests.utils import onenv_utils


def pytest_addoption(parser):
    parser.addoption('--test-type', action='store', default='oneclient',
                     help='type of test (oneclient, env_up, '
                          'packaging, gui)')

    parser.addoption('--local', action='store_true',
                     help='If specified tests are assumed to be stared '
                          'on local machine')
    parser.addoption('--pull-only-missing-images', action='store_true',
                     help='By default all test scenarios force pulling docker '
                          'images even if they are already present on host. '
                          'When this option is passed only missing images '
                          'will be downloaded.')
    parser.addoption('--ignore-xfail', action='store_true',
                     help='Ignores xfail mark')
    parser.addoption('--env-file', action='store', default=None,
                     help='description of environment that will be tested')

    parser.addoption('--oz-image', action='store', help='onezone image'
                                                        'to use in tests')
    parser.addoption('--op-image', action='store', help='oneprovider image'
                                                        'to use in tests')
    parser.addoption('--oc-image', action='store', help='oneclient image'
                                                        'to use in tests')
    parser.addoption('--rest-cli-image', action='store',
                     help='rest cli image to use in tests')
    parser.addoption('--openfaas-pod-status-monitor-image', action='store',
                     help='OpenFaaS pod status monitor image to use in tests')
    parser.addoption('--openfaas-lambda-result-streamer-image', action='store',
                     help='OpenFaaS lambda result streamer image to use in tests')
    parser.addoption('--sources', action='store_true',
                     help='If present run environment using sources')

    parser.addoption('--timeout', action='store',
                     help='onenv wait timeout')

    group = parser.getgroup('onedata', description='option specific '
                                                   'to onedata tests')

    group.addoption('--admin', default=['admin', 'password'], nargs=2,
                    help='admin credentials in form: -u username password',
                    metavar=('username', 'password'), dest='admin')
    group.addoption('--preserve-users', action='store_true',
                    help='If set users created in previous tests will not be '
                         'removed if their names collide with the names '
                         'of users that will be created in current test. '
                         'Instead such a test will be skipped.')
    group.addoption('--add-test-domain', action='store_true',
                    help='If set test domain is added to /etc/hosts')

    onenv = parser.getgroup('onenv', description='option specific to onenv')
    onenv.addoption('--local-charts-path', action='store',
                    help='Path to local charts')
    onenv.addoption('--no-clean', action='store_true',
                    help='If present prevents cleaning environment created '
                         'by one-env')
    onenv.addoption('--gui-pkg-verification', action='store_true',
                    help='enables verification of GUI packages')


def pytest_generate_tests(metafunc):
    if metafunc.config.option.test_type:
        test_type = metafunc.config.option.test_type

        if test_type in ['gui', 'mixed', 'onedata_fs', 'oneclient', 'performance']:
            if test_type == 'gui':
                default_env_file = '1oz_1op_deployed'
            else:
                default_env_file = '1oz_1op_1oc'

            env_file = metafunc.config.getoption('env_file')
            if env_file:
                metafunc.parametrize('env_description_file', [env_file],
                                     scope='session')
            else:
                metafunc.parametrize('env_description_file', [default_env_file],
                                     scope='session')
        elif test_type in ['upgrade']:
            env_file = metafunc.config.getoption('env_file')
            if env_file:
                with open(env_file, 'r') as f:
                    test_config = yaml.load(f)
                scenarios = test_config['scenarios']
                metafunc.parametrize(
                    'env_description_file',
                    [env_file for env_file in scenarios],
                    scope='session'
                )
            else:
                raise RuntimeError("In upgrade tests --env-file option must be provided")


@pytest.fixture(scope='session')
def test_config(request):
    """Loaded yaml with test config"""
    test_type = get_test_type(request)
    if test_type == 'upgrade':
        with open(request.config.option.env_file, 'r') as f:
            return yaml.load(f)
    return {}


@pytest.fixture(scope='session')
def entities_config(request, env_desc):
    file_name = env_desc.get('entities_config')
    config_dir_path = ENTITIES_CONFIG_DIR.get(get_test_type(request))
    config_path = os.path.join(config_dir_path, file_name)
    with open(config_path) as config_file:
        return yaml.load(config_file)


@pytest.fixture(autouse=True)
def onepanel_credentials(users, hosts, emergency_passphrase):
    creds = users['onepanel'] = AdminUser(
        hosts['onezone']['hostname'], 'onepanel', emergency_passphrase)
    return creds


@pytest.fixture(autouse=True)
def emergency_passphrase(users, hosts):
    zone_pod_name = hosts['onezone']['pod-name']
    zone_pod = onenv_utils.match_pods(zone_pod_name)[0]
    passphrase = onenv_utils.get_env_variable(zone_pod,
                                              'ONEPANEL_EMERGENCY_PASSPHRASE')
    return passphrase


@pytest.fixture(autouse=True)
def admin_credentials(request, users, hosts):
    admin_username, admin_password = request.config.getoption('admin')
    admin_user = users[admin_username] = AdminUser(hosts['onezone']['hostname'], admin_username,
                                                   admin_password)
    return admin_user


@pytest.fixture(scope='session')
def users():
    """Dictionary with users credentials"""
    return {}


@pytest.fixture()
def clients():
    """Dictionary with users clients, e.g. {client1: Client()}"""
    return {}


@pytest.fixture
def groups():
    """Mapping group name to group id, e.g. {group1: UEIHSdft743dfjKEUgr}"""
    return {}


@pytest.fixture
def spaces():
    """Mapping space name to space id, e.g. {space1: UEIHSdft743dfjKEUgr}"""
    return {}


@pytest.fixture
def storages():
    """Mapping storage name to storage id, e.g. {st1: UEIHSdft743dfjKEUgr}"""
    return {}


@pytest.fixture
def harvesters():
    """Mapping harvester name to harvester id, e.g. {st1: UEIHSdft743d}"""
    return {}


@pytest.fixture
def context():
    """Dict to use when one wants to store sth between steps."""
    return {}


@pytest.fixture(scope='session')
def hosts():
    """Dict to use to store information about services."""
    return {}


@pytest.fixture
def tokens():
    """Dict to use to store information about tokens, e.g. {'token1': {
    'token_id': HGS2783GYIS, 'token': HDSGUFGJY875381FGJFSU}}"""
    return {}


@pytest.fixture
def rm_users(request):
    return not request.config.getoption('--preserve-users')


@pytest.fixture(scope='session')
def env_description_abs_path(request, env_description_file):
    env_dir = ENV_DIRS.get(get_test_type(request))
    absolute_path = absolute_path_to_env_file(env_dir, env_description_file)
    return absolute_path


@pytest.fixture(scope='session')
def env_desc(env_description_abs_path):
    with open(env_description_abs_path, 'r') as env_desc_file:
        return yaml.load(env_desc_file)


@pytest.fixture(scope='session')
def previous_env():
    return {}


@pytest.fixture(scope='session', autouse=True)
def maybe_start_env(env_description_abs_path, hosts, request, env_desc, users, previous_env, 
                    test_config):
    test_type = get_test_type(request)

    if _should_start_new_env(env_description_abs_path, previous_env):
        start_test_env(request, test_type, env_desc, hosts, users, env_description_abs_path,
                       test_config, previous_env)

    return


def _should_start_new_env(env_description_abs_path, previous_env):
    previous_env_path = previous_env.get('env_path', '')
    previous_env_started = previous_env.get('started', False)
    start_env = True

    # Check which environment was started last time to avoid starting
    # the same env multiple times
    if previous_env_path == env_description_abs_path:
        if previous_env_started:
            start_env = False
        else:
            # Since the same env failed to start last time assume
            # problem with k8s - skip tests
            pytest.skip('Environment error.')
    else:
        start_env = True
        previous_env['env_path'] = env_description_abs_path

    return start_env


def handle_env_init_error(request, env_description_abs_path, error_msg):
    export_logs(request, env_description_abs_path)
    clean_env()
    pytest.skip(error_msg)


def start_test_env(request, test_type, env_desc, hosts, users, env_description_abs_path,
                   test_config, previous_env):
    patch_path = ''
    scenario_path = ''
    if test_type in ['gui']:
        scenario_path = env_description_abs_path
    elif test_type in ['oneclient', 'mixed']:
        scenario_path = scenario_abs_path(request, env_desc)
    elif test_type in ['onedata_fs', 'performance', 'upgrade']:
        scenario_path = scenario_abs_path(request, env_desc)
        patch = env_desc.get('patch')
        patch_dir_path = PATCHES_DIR.get(get_test_type(request))
        patch_path = os.path.join(patch_dir_path, patch)

    result = start_environment(
        scenario_path, request, hosts, patch_path, users, test_config
    )
    if result != 'ok':
        previous_env['started'] = False
        handle_env_init_error(request, env_description_abs_path, str(result))
    else:
        previous_env['started'] = True


@pytest.fixture(scope='session')
def scenario_abs_path(request, env_desc):
    scenario = env_desc.get('scenario')
    scenarios_dir_path = SCENARIO_DIRS.get(get_test_type(request))
    return os.path.abspath(os.path.join(scenarios_dir_path,
                                        scenario))


def get_test_type(request):
    return request.config.getoption('test_type')


def export_logs(request, env_description_abs_path=None, logdir_prefix=''):
    test_type = get_test_type(request)
    logdir_path = LOGDIRS.get(test_type)

    if test_type in ['oneclient', 'upgrade']:
        try:
            feature_name = request.module.__name__.split('.')[-1]
            test_path = os.path.join(get_file_name(env_description_abs_path),
                                     feature_name)
        except AttributeError:
            test_path = "test"
        logdir_path = make_logdir(logdir_path, test_path)
    else:
        timestamped_logdirs = os.listdir(logdir_path)
        latest_logdir = max(timestamped_logdirs, key=extract_timestamp)
        logdir_path = os.path.join(logdir_path, latest_logdir)

    if logdir_prefix:
        dirpath, name = os.path.split(logdir_path)
        logdir_path = os.path.join(dirpath, logdir_prefix + '.' + name)
    onenv_utils.run_onenv_command('export', [logdir_path, '-c', CLIENT_POD_LOGS_DIR], fail_with_error=False)


def extract_timestamp(filename):
    s = re.findall(r'\d+\.\d+$', filename)
    return float(s[0]) if s else -1


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
