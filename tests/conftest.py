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
import copy
import datetime
import sys
import time
from copy import deepcopy

from tests import (ENV_DIRS, SCENARIO_DIRS, PATCHES_DIR, ENTITIES_CONFIG_DIR,
                   LOGDIRS)
from tests.utils import CLIENT_POD_LOGS_DIR
from tests.utils.user_utils import AdminUser
from tests.utils.environment_utils import start_environment, clean_env
from tests.utils.path_utils import (get_file_name, absolute_path_to_env_file,
                                    make_logdir)
from tests.utils import onenv_utils

from _pytest.fixtures import FixtureLookupError
from selenium.webdriver import Chrome

from selenium.webdriver.support.event_firing_webdriver import \
    EventFiringWebDriver


# ============================================================================
# PYTEST CONFIGURATION
# =============================================================================


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
    parser.addoption('--file-mode', action='store', default='regular',
                     help="""Determines how files in a test are created:
                            * regular - a file is created as standard regular file (default);
                            * hardlink - a file is created as a hardlink to a 
                            regular file in a space, all created files are hardlinks to a different file;
                            * symlink - a file is created as a symlink to a 
                            regular file in a space, all created files are symlinks to a different file""")

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

    _capture_choices = ('never', 'failure', 'always')
    parser.addini('selenium_capture_debug',
                  help='when debug is captured {0}'.format(_capture_choices),
                  default=os.getenv('SELENIUM_CAPTURE_DEBUG', 'failure'))

    group = parser.getgroup('selenium', 'selenium')
    group.addoption('--xvfb-recording',
                    help='record tests (possible options: all | none | failed) '
                         'using ffmpeg and save results to <logdir>/movies/',
                    dest='xvfb_recording',
                    choices=['all', 'none', 'failed'],
                    default='none')


def pytest_generate_tests(metafunc):
    if metafunc.config.option.test_type:
        test_type = metafunc.config.option.test_type

        if test_type in ['gui', 'mixed', 'onedata_fs', 'oneclient',
                         'performance']:
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
                    test_config = yaml.load(f, yaml.Loader)
                scenarios = test_config['scenarios']
                metafunc.parametrize(
                    'env_description_file',
                    [env_file for env_file in scenarios],
                    scope='session'
                )
            else:
                raise RuntimeError(
                    "In upgrade tests --env-file option must be provided")


def pytest_configure(config):
    if hasattr(config, 'slaveinput'):
        return  # xdist slave
    config.addinivalue_line(
        'markers', 'capabilities(kwargs): add or change existing '
                   'capabilities. specify capabilities as keyword arguments, for example '
                   'capabilities(foo=''bar'')')


def pytest_report_header(config, start_path):
    driver = config.getoption('driver')
    if driver is not None:
        return 'driver: {0}'.format(driver)


# =============================================================================
# PYTEST FIXTURES
# =============================================================================


@pytest.fixture(scope='session')
def test_config(request):
    """Loaded yaml with test config"""
    test_type = get_test_type(request)
    if test_type == 'upgrade':
        with open(request.config.option.env_file, 'r') as f:
            return yaml.load(f, yaml.Loader)
    return {}


@pytest.fixture(scope='session')
def entities_config(request, env_desc):
    file_name = env_desc.get('entities_config')
    config_dir_path = ENTITIES_CONFIG_DIR.get(get_test_type(request))
    config_path = os.path.join(config_dir_path, file_name)
    with open(config_path) as config_file:
        return yaml.load(config_file, yaml.Loader)


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
    admin_user = users[admin_username] = AdminUser(hosts['onezone']['hostname'],
                                                   admin_username,
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
def inventories():
    """Mapping inventory name to inventory id, e.g.
    {inventory1: UEIHSdft743dfjKEUgr}"""
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
def workflows():
    """Dict to use to store information about uploaded to zone workflow schemas,
    e.g. {'workflow_name': 'workflow_id'}"""
    return {}


@pytest.fixture
def workflow_executions():
    """Dict to use to store information about execution workflow id with
    its name and input args, e.g. {'wid': {name: [arg1, arg2, ...]}}"""
    return {}


@pytest.fixture
def rm_users(request):
    return not request.config.getoption('--preserve-users')


@pytest.fixture
def selenium(request):
    """Returns a WebDriver instance based on options and capabilities"""
    return {'request': request}


@pytest.fixture(scope='session')
def session_capabilities(request, variables):
    """Returns combined capabilities from pytest-variables and command line"""
    capabilities = variables.get('capabilities', {})
    for capability in request.config.getoption('capabilities'):
        capabilities[capability[0]] = capability[1]
    return capabilities


@pytest.fixture
def capabilities(request, session_capabilities):
    """Returns combined capabilities"""
    capabilities = copy.deepcopy(session_capabilities)  # make a copy
    capabilities_marker = request.node.get_closest_marker('capabilities')
    if capabilities_marker is not None:
        # add capabilities from the marker
        capabilities.update(capabilities_marker.kwargs)
    return capabilities


# ============================================================================
# WEBDRIVER
# ============================================================================


@pytest.fixture
def driver(request):
    """Return a factory function creating WebDriver instances.
    """
    driver_factory = request.getfixturevalue('chrome_driver')

    event_listener = request.config.getoption('event_listener')
    if event_listener:
        # Import the specified event listener and wrap the driver instance
        mod_name, class_name = event_listener.rsplit('.', 1)
        mod = __import__(mod_name, fromlist=[class_name])
        event_listener = getattr(mod, class_name)

    @factory
    def _get_instance():
        """Return WebDriver instance based on given options.
        """
        web_driver = driver_factory.get_instance()
        if event_listener and not isinstance(web_driver, EventFiringWebDriver):
            web_driver = EventFiringWebDriver(web_driver, event_listener())

        request.node._driver = web_driver
        request.addfinalizer(web_driver.quit)
        return web_driver

    return _get_instance


@pytest.fixture
def config_driver():
    def _configure(driver):
        return driver

    return _configure


@pytest.fixture
def chrome_driver(capabilities):
    """Return a factory function creating Chrome WebDriver instances.
    """

    @factory
    def _get_instance():
        """Return Chrome WebDriver instance based on given options.
        """
        kwargs = {}
        if capabilities:
            kwargs['options'] = deepcopy(capabilities['options'])
        return Chrome(**kwargs)

    return _get_instance


def factory(fun):
    if 'get_instance' in dir(fun):
        raise AttributeError('object {:s} already has "get_instance" '
                             'attribute'.format(fun.__name__))
    else:
        fun.get_instance = lambda *args, **kwargs: fun(*args, **kwargs)
        return fun


# ============================================================================
# TEST REPORT
# ============================================================================


_movies = set()


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
    onenv_utils.run_onenv_command('export',
                                  [logdir_path, '-c', CLIENT_POD_LOGS_DIR],
                                  fail_with_error=False)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    summary = []
    extra = getattr(report, 'extra', [])
    driver = getattr(item, '_driver', None)
    xfail = hasattr(report, 'wasxfail')
    xvfb_rec = item.config.option.xvfb_recording
    failure = (report.skipped and xfail) or (report.failed and not xfail)
    when = item.config.getini('selenium_capture_debug').lower()
    capture_debug = when == 'always' or (when == 'failure' and failure)
    if driver is not None:
        if capture_debug:
            exclude = item.config.getini('selenium_exclude_debug').lower()
            if 'url' not in exclude:
                _gather_url(item, report, driver, summary, extra)
            if 'screenshot' not in exclude:
                _gather_screenshot(item, report, driver, summary, extra)
            if 'html' not in exclude:
                _gather_html(item, report, driver, summary, extra)
            if 'logs' not in exclude:
                _gather_logs(item, report, driver, summary, extra)
            item.config.hook.pytest_selenium_capture_debug(
                item=item, report=report, extra=extra)

        if xvfb_rec != 'none':
            movie_name = '{name}.mp4'.format(name=item.name)
            if (xvfb_rec == 'failed') and (
                    movie_name not in _movies) and not failure:
                logdir = os.path.dirname(item.config.option.htmlpath)
                movie_path = os.path.join(logdir, 'movies', movie_name)
                if os.path.isfile(movie_path):
                    os.remove(movie_path)
            else:
                _movies.add(movie_name)

        item.config.hook.pytest_selenium_runtest_makereport(
            item=item, report=report, summary=summary, extra=extra)
    if summary:
        report.sections.append(('pytest-selenium', '\n'.join(summary)))
    report.extra = extra


def _gather_url(item, report, driver, summary, extra):
    try:
        url = driver.current_url
    except Exception as e:
        summary.append('WARNING: Failed to gather URL: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        # add url to the html report
        extra.append(pytest_html.extras.url(url))
    summary.append('URL: {0}'.format(url))


def _gather_screenshot(item, report, driver, summary, extra):
    try:
        screenshot = driver.get_screenshot_as_base64()
    except Exception as e:
        summary.append('WARNING: Failed to gather screenshot: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        # add screenshot to the html report
        extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))


def _gather_html(item, report, driver, summary, extra):
    try:
        html = driver.page_source
    except Exception as e:
        summary.append('WARNING: Failed to gather HTML: {0}'.format(e))
        return
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is not None:
        # add page source to the html report
        extra.append(pytest_html.extras.text(html, 'HTML'))


# TODO VFS-12302 implement gathering browser logs
def _gather_logs(item, report, driver, summary, extra):
    try:
        types = driver.log_types
    except Exception as e:
        # note that some drivers may not implement log types
        summary.append('WARNING: Failed to gather log types: {0}'.format(e))
        return
    for name in types:
        try:
            log = driver.get_log(name)
        except Exception as e:
            summary.append('WARNING: Failed to gather {0} log: {1}'.format(
                name, e))
            return
        pytest_html = item.config.pluginmanager.getplugin('html')
        formatted_logs = ''

        if pytest_html is not None:
            extra.append(pytest_html.extras.text(
                '{}{}'.format(format_log(log), formatted_logs),
                '%s Log' % name.title()))


def format_log(log):
    timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
    entries = [u'{0} {1[level]} - {1[message]}'.format(
        datetime.utcfromtimestamp(entry['timestamp'] / 1000.0).strftime(
            timestamp_format), entry).rstrip() for entry in log]
    log = '\n'.join(entries)
    return log


def extract_timestamp(filename):
    s = re.findall(r'\d+\.\d+$', filename)
    return float(s[0]) if s else -1


# =============================================================================
# ENVIRONMENT
# =============================================================================


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


def start_test_env(request, test_type, env_desc, hosts, users,
                   env_description_abs_path,
                   test_config, previous_env, scenario_abs_path):
    patch_path = ''
    scenario_path = ''
    if test_type in ['gui']:
        scenario_path = env_description_abs_path
    elif test_type in ['oneclient', 'mixed']:
        scenario_path = scenario_abs_path
    elif test_type in ['onedata_fs', 'performance', 'upgrade']:
        scenario_path = scenario_abs_path
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
def env_description_abs_path(request, env_description_file):
    env_dir = ENV_DIRS.get(get_test_type(request))
    absolute_path = absolute_path_to_env_file(env_dir, env_description_file)
    return absolute_path


@pytest.fixture(scope='session')
def env_desc(env_description_abs_path):
    with open(env_description_abs_path, 'r') as env_desc_file:
        return yaml.load(env_desc_file, yaml.Loader)


@pytest.fixture(scope='session')
def previous_env():
    return {}


@pytest.fixture(scope='session', autouse=True)
def maybe_start_env(env_description_abs_path, hosts, request, env_desc, users,
                    previous_env,
                    test_config, scenario_abs_path):
    test_type = get_test_type(request)

    if _should_start_new_env(env_description_abs_path, previous_env):
        start_test_env(request, test_type, env_desc, hosts, users,
                       env_description_abs_path,
                       test_config, previous_env, scenario_abs_path)

    return


@pytest.fixture(scope='session')
def scenario_abs_path(request, env_desc):
    scenario = env_desc.get('scenario')
    scenarios_dir_path = SCENARIO_DIRS.get(get_test_type(request))
    return os.path.abspath(os.path.join(scenarios_dir_path,
                                        scenario))


# ============================================================================
# Miscellaneous.
# ============================================================================


def get_test_type(request):
    return request.config.getoption('test_type')


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
    if request.node.get_closest_marker('skip_env'):
        env = get_file_name(env_description_file)
        args = request.node.get_closest_marker('skip_env').kwargs
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
    if request.node.get_closest_marker('xfail_env'):
        env = get_file_name(env_description_file)
        args = request.node.get_closest_marker('xfail_env').kwargs
        reason = args['reason']
        arg_envs = [get_file_name(e) for e in args['envs']]
        ignore = request.config.getoption("--ignore-xfail")
        if env in arg_envs and not ignore:
            request.node.add_marker(pytest.mark.xfail(
                reason='xfailed on env: {env} with reason: {reason}'
                .format(env=env, reason=reason)))


def select_browser(selenium, browser_id):
    browser = selenium[browser_id]
    selenium['request'].node._driver = browser
    return browser


def split_class_and_test_names(nodeid):
    """Returns the class and method name from the current test"""
    names = nodeid.split('::')
    names[0] = names[0].replace('/', '.')
    names = [x.replace('.py', '') for x in names if x != '()']
    classnames = names[:-1]
    classname = '.'.join(classnames)
    name = names[-1]
    return (classname, name)
