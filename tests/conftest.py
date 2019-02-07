"""
Definitions of fixtures used in acceptance tests.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import re
import subprocess as sp

import yaml
import pytest

from environment import docker
from tests.utils.path_utils import (get_file_name, absolute_path_to_env_file,
                                    make_logdir)
from tests.utils.user_utils import User
from tests.utils.onenv_utils import (run_onenv_command, init_helm,
                                     client_alias_to_pod_mapping,
                                     service_name_to_alias_mapping,
                                     deployment_data_path)
from tests import (CONFIG_FILES, PANEL_REST_PORT, ENV_DIRS, SCENARIO_DIRS,
                   LANDSCAPE_DIRS, LOGDIRS)


def pytest_addoption(parser):
    parser.addoption('--test-type', action='store', default='oneclient',
                     help='type of test (oneclient, env_up, '
                          'packaging, gui)')

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
    parser.addoption('--luma-image', action='store', help='luma image'
                                                          'to use in tests')
    parser.addoption('--rest-cli-image', action='store',
                     help='rest cli image to use in tests')
    parser.addoption('--sources', action='store_true',
                     help='If present run environment using sources')

    parser.addoption('--timeout', action='store',
                     help='onenv wait timeout')

    group = parser.getgroup('onedata', description='option specific '
                                                   'to onedata tests')

    group.addoption('--add-test-domain', action='store_true',
                    help='If set test domain is added to /etc/hosts')

    onenv = parser.getgroup('onenv', description='option specific to onenv')
    onenv.addoption('--local-charts-path', action='store',
                    help='Path to local charts')
    onenv.addoption('--no-clean', action='store_true',
                    help='If present prevents cleaning environment created '
                         'by one-env')


def pytest_generate_tests(metafunc):
    if metafunc.config.option.test_type:
        test_type = metafunc.config.option.test_type

        if test_type in ['gui', 'mixed']:
            if test_type == 'mixed':
                default_env_file = '1oz_1op_1oc'
            else:
                default_env_file = '1oz_1op_deployed'

            env_file = metafunc.config.getoption('env_file')
            if env_file:
                metafunc.parametrize('env_description_file', [env_file],
                                     scope='session')
            else:
                metafunc.parametrize('env_description_file',
                                     [default_env_file], scope='session')

        elif test_type == 'oneclient':
            env_file = metafunc.config.getoption('env_file')
            if env_file:
                metafunc.parametrize('env_description_file', [env_file],
                                     scope='module')
            else:
                with open(CONFIG_FILES.get(test_type), 'r') as f:
                    test_config = yaml.load(f)

                test_file = metafunc.module.__name__.split('.')[-1]
                if test_file in test_config:
                    metafunc.parametrize(
                        'env_description_file',
                        [env_file for env_file in test_config[test_file]],
                        scope='module'
                    )


@pytest.fixture(scope='module')
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
def context():
    """Dict to use when one wants to store sth between steps."""
    return {}


@pytest.fixture(scope='module')
def hosts():
    """Dict to use to store information about services."""
    return {}


def add_etc_hosts_entries(service_ip, service_host):
    sp.call('sudo bash -c "echo {} {} >> /etc/hosts"'.format(
        service_ip, service_host), shell=True)


def set_debug(container_id, service_name, service_type, sources_data=None):
    if sources_data:
        set_debug_fmt = (r'echo {{\"debug\": true}} > '
                         r'{}')
        app_cfg_fmt = '_build/default/rel/{}/data/gui_static/app-config.json'
        worker_name = ('op-worker' if 'provider' in service_type else
                       'oz-worker')
        app_cfg_path = app_cfg_fmt.format(worker_name.replace('-', '_'))
        for pod_name, pod_cfg in sources_data.items():
            if service_name in pod_name:
                worker_path = pod_cfg.get(worker_name)
                set_debug_cmd = set_debug_fmt.format(os.path.join(worker_path,
                                                                  app_cfg_path))
                docker.exec_(container_id, set_debug_cmd)

    else:
        set_debug_fmt = (r'echo {{\"debug\": true}} > '
                         r'/var/lib/{}_worker/gui_static/app-config.json')
        set_debug_cmd = set_debug_fmt.format('op' if 'provider' in
                                                     service_type else 'oz')
        docker.exec_(container_id, set_debug_cmd)


def parse_oz_op_cfg(pod_name, pod_cfg, service_type, add_test_domain, hosts,
                    sources_data):
    alias = service_name_to_alias_mapping(pod_name)
    name, hostname, ip, container_id = (pod_cfg.get('name'),
                                        pod_cfg.get('domain'),
                                        pod_cfg.get('ip'),
                                        pod_cfg.get('container-id'))
    hosts[alias] = {'service-type': service_type,
                    'name': name,
                    'hostname': hostname,
                    'ip': ip,
                    'container-id': container_id,
                    'panel':
                        {'hostname': '{}:{}'.format(hostname,
                                                    PANEL_REST_PORT)}
                    }
    set_debug(container_id, name, service_type, sources_data)
    if add_test_domain and service_type == 'oneprovider':
        add_etc_hosts_entries(ip, '{}.test'.format(hostname))


def parse_client_cfg(pod_name, pod_cfg, hosts):
    ip, container_id, provider_host = (pod_cfg.get('ip'),
                                       pod_cfg.get('container-id'),
                                       pod_cfg.get('provider-host'))

    client_alias = client_alias_to_pod_mapping().get(pod_name)
    hosts[client_alias] = {'ip': ip,
                           'container-id': container_id,
                           'provider-host': provider_host}


def parse_hosts_cfg(pods_cfg, hosts, request):
    sources_data = {}
    data_path = deployment_data_path()
    if os.path.isfile(data_path):
        with open(data_path, 'r') as deployment_data_file:
            deployment_data = yaml.load(deployment_data_file)
            sources_data = deployment_data.get('sources')

    for pod_name, pod_cfg in pods_cfg.items():
        service_type = pod_cfg['service-type']
        if service_type in ['onezone', 'oneprovider']:
            parse_oz_op_cfg(pod_name, pod_cfg, service_type,
                            request.config.getoption('--add-test-domain'),
                            hosts, sources_data)

        elif service_type == 'oneclient':
            parse_client_cfg(pod_name, pod_cfg, hosts)


def parse_users_cfg(patch_path, users, hosts):
    with open(patch_path, 'r') as patch_file:
        patch_cfg = yaml.load(patch_file)
        users_cfg = patch_cfg.get('users')

        for user_cfg in users_cfg:
            user_name = user_cfg.get('name')
            password = user_cfg.get('password')
            new_user = users[user_name] = User(user_name, password)
            new_user.token = new_user.create_token(hosts['onezone']['ip'])


@pytest.fixture(scope='module', autouse=True)
def env_description_abs_path(request, env_description_file):
    env_dir = ENV_DIRS.get(get_test_type(request))
    absolute_path = absolute_path_to_env_file(env_dir, env_description_file)
    return absolute_path


@pytest.fixture(scope='module', autouse=True)
def env_desc(env_description_abs_path, hosts, request, users):
    """
    Sets up environment and returns environment description.
    """
    test_type = get_test_type(request)

    if test_type in ['gui']:
        # For now gui tests do not use onenv patch
        start_environment(env_description_abs_path, request, hosts, '',
                          users, env_description_abs_path)
        return ''

    elif test_type == 'mixed':
        with open(env_description_abs_path, 'r') as env_desc_file:
            env_desc = yaml.load(env_desc_file)

        scenario = env_desc.get('scenario')
        scenarios_dir_path = SCENARIO_DIRS.get(get_test_type(request))
        scenario_path = os.path.abspath(os.path.join(scenarios_dir_path,
                                                     scenario))
    
        start_environment(scenario_path, request, hosts, '',
                          users, env_description_abs_path)
        return env_desc

    elif test_type == 'oneclient':
        with open(env_description_abs_path, 'r') as env_desc_file:
            env_desc = yaml.load(env_desc_file)

        scenario = env_desc.get('scenario')
        scenarios_dir_path = SCENARIO_DIRS.get(
            get_test_type(request))
        scenario_path = os.path.abspath(
            os.path.join(scenarios_dir_path, scenario))

        patch = env_desc.get('patch')
        patch_dir_path = LANDSCAPE_DIRS.get(
            get_test_type(request))
        patch_path = os.path.join(patch_dir_path, patch)

        start_environment(scenario_path, request, hosts, patch_path, users,
                          env_description_abs_path)
        return env_desc


def parse_up_args(request, scenario_path):
    up_args = []

    oz_image = request.config.getoption('--oz-image')
    op_image = request.config.getoption('--op-image')
    oc_image = request.config.getoption('--oc-image')
    luma_image = request.config.getoption('--luma-image')
    rest_cli_image = request.config.getoption('--rest-cli-image')
    sources = request.config.getoption('--sources')
    timeout = request.config.getoption('--timeout')
    local_charts_path = request.config.getoption('--local-charts-path')

    if oz_image:
        up_args.extend(['-zi', oz_image])
    if op_image:
        up_args.extend(['-pi', op_image])
    if oc_image:
        up_args.extend(['-ci', oc_image])
    if luma_image:
        up_args.extend(['-li', luma_image])
    if rest_cli_image:
        up_args.extend(['-ri', rest_cli_image])
    if sources:
        up_args.append('-s')
    if local_charts_path:
        up_args.extend(['-lcp', local_charts_path])
    if timeout:
        up_args.extend(['--timeout', timeout])

    up_args.extend(['{}'.format(scenario_path)])
    return up_args


def parse_patch_args(request, patch_path):
    patch_args = []
    local_charts_path = request.config.getoption('--local-charts-path')

    if local_charts_path:
        patch_args.extend(['-lcp', local_charts_path])

    patch_args.extend(['--patch', patch_path])
    return patch_args


def parse_wait_args(request):
    wait_args = []

    timeout = request.config.getoption('--timeout')
    if timeout:
        wait_args.extend(['--timeout', timeout])
    return wait_args


def start_environment(scenario_path, request, hosts, patch_path,
                      users, env_description_abs_path):
    init_helm()
    clean = False if request.config.getoption('--no-clean') else True

    if clean:
        up_args = parse_up_args(request, scenario_path)
        output, ret = run_onenv_command('up', up_args)
        if ret != 0:
            handle_env_init_error(request, env_description_abs_path, 'up',
                                  output)

        wait_args = parse_wait_args(request)
        run_onenv_command('wait', wait_args)

    status_output, _ = run_onenv_command('status')
    status_output = yaml.load(status_output.decode('utf-8'))

    env_ready = status_output.get('ready')
    if not env_ready:
        handle_env_init_error(request, env_description_abs_path, 'status',
                              env_ready)

    pods_cfg = status_output['pods']
    parse_hosts_cfg(pods_cfg, hosts, request)
    run_onenv_command('hosts')

    if patch_path and clean:
        patch_args = parse_patch_args(request, patch_path)
        run_onenv_command('patch', patch_args)
        run_onenv_command('wait')

    if patch_path:
        parse_users_cfg(patch_path, users, hosts)

    test_type = get_test_type(request)
    if test_type == 'oneclient' and clean:
        def fin():
            run_onenv_command('clean', ['-a', '-v'])

        request.addfinalizer(fin)


def handle_env_init_error(request, env_description_abs_path, command, output):
    export_logs(request, env_description_abs_path)
    run_onenv_command('clean', ['-a', '-v'])
    pytest.skip('Environment error: Onenv command {} failed.'
                'Captured stdout: {}.'
                .format(command, output))


def get_test_type(request):
    return request.config.getoption('test_type')


def extract_timestamp(filename):
    s = re.findall('\d+\.\d+$', filename)
    return float(s[0]) if s else -1


def export_logs(request, env_description_abs_path=None):
    test_type = get_test_type(request)
    logdir_path = LOGDIRS.get(test_type)

    if test_type == 'oneclient':
        feature_name = request.module.__name__.split('.')[-1]
        test_path = os.path.join(get_file_name(env_description_abs_path),
                                 feature_name)
        logdir_path = make_logdir(logdir_path, test_path)
    else:
        timestamped_logdirs = os.listdir(logdir_path)
        latest_logdir = max(timestamped_logdirs, key=extract_timestamp)
        logdir_path = os.path.join(logdir_path, latest_logdir)

    run_onenv_command('export', [logdir_path])


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
