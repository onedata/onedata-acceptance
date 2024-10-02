"""
Define fixtures used in web GUI acceptance/behavioral tests.
"""
__author__ = "Jakub Liput, Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import re
import errno
from time import time
import subprocess as sp
from collections import defaultdict

from selenium import webdriver
from pytest import fixture, UsageError, skip, hookimpl

from tests.utils.path_utils import make_logdir
from tests import LOGDIRS
import tests.utils.xvfb_utils as xvfb_utils
from tests.gui.utils.generic import suppress
from tests.conftest import export_logs
from _pytest.fixtures import FixtureLookupError
from tests.utils.ffmpeg_utils import start_recording, stop_recording
from tests.oneclient.steps.environment_steps import unmock_archive_verification


SELENIUM_IMPLICIT_WAIT = 0

# use this const when using: WebDriverWait(selenium, WAIT_FRONTEND).until(lambda s: ...)
# when waiting for frontend changes
WAIT_FRONTEND = 4

# use this const when using: WebDriverWait(selenium, WAIT_BACKEND).until(lambda s: ...)
# when waiting for backend changes
WAIT_BACKEND = 15

# use this const when using: WebDriverWait(selenium, WAIT_NORMAL_UPLOAD).until(lambda s: ...)
# when waiting for normal uploads to finish
WAIT_NORMAL_UPLOAD = 60

# use this const when using: WebDriverWait(selenium, WAIT_EXTENDED_UPLOAD).until(lambda s: ...)
# when waiting for extended uploads to finish
WAIT_EXTENDED_UPLOAD = 1500


# ============================================================================
# PYTEST CONFIGURATION
# =============================================================================


def pytest_configure(config):
    """Set default path for Selenium HTML report if explicit '--html=' not specified"""
    htmlpath = config.option.htmlpath
    if htmlpath is None:
        import os
        test_type = config.option.test_type
        logdir = make_logdir(LOGDIRS.get(test_type), 'report')
        config.option.htmlpath = os.path.join(logdir, 'report.html')


def pytest_addoption(parser):
    selenium_group = parser.getgroup('selenium', 'selenium')
    selenium_group.addoption('--xvfb',
                             action='store_true',
                             help='run Xvfb for tests')
    selenium_group.addoption('--no-mosaic-filter',
                             action='store_true',
                             help='turn off mosaic filter if recording tests '
                                  'with multiple browsers')


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, rep.when + '_xvfb_recorder', rep)


def pytest_collection_modifyitems(items):
    first = []
    second = []
    second_to_last = []
    last = []
    rest = []

    run_first = ('test_cluster_deployment',
                 )
    run_second = ('test_support_space', 'test_revoke_space_support')
    run_second_to_last = ('test_user_changes_provider_name_and_domain',
                          )
    run_last = ('test_user_deregisters_provider',
                )
    for item in items:
        item.name = re.sub('{.*}', '', item.name)
        item.name = re.sub('<.*>', '', item.name)

    for item in items:
        for suite_scenarios, run_suite in ((run_first, first),
                                           (run_second, second),
                                           (run_second_to_last, second_to_last),
                                           (run_last, last)):
            found_suite = False
            for scenario_name in suite_scenarios:
                if scenario_name in item.nodeid:
                    run_suite.append(item)
                    found_suite = True
                    break

            if found_suite:
                break
        else:
            rest.append(item)

    first.extend(second)
    first.extend(rest)
    first.extend(second_to_last)
    first.extend(last)
    items[:] = first


def pytest_bdd_before_scenario(request, feature, scenario):
    print(f"\n=================================================================")
    print(f"- Executing scenario '{scenario.name}'")
    print(f"- from feature '{feature.name}'")
    print(f"-----------------------------------------------------------------")


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    print(f"-- Executing step: {format_step_name(step)}")


def pytest_bdd_after_scenario(request, feature, scenario):
    print(f"=================================================================")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f"--- STEP FAILED on {step}")
    print(f'--- Exception: {exception}\n')


def format_step_name(step_name):
    step_name = step_name.name.split('\n')
    if len(step_name) > 1:
        return step_name[0] + ' (...)'
    else:
        return step_name[0]

# =============================================================================
# PYTEST FIXTURES
# =============================================================================


@fixture(autouse=True, scope='module')
def finalize(request):
    yield
    export_logs(request)


@fixture(scope='session')
def numerals():
    return {'first': 0,
            'second': 1,
            'third': 2,
            'fourth': 3,
            'fifth': 4,
            'sixth': 5,
            'seventh': 6,
            'eighth': 7,
            'ninth': 8,
            'tenth': 9,
            'last': -1}


@fixture(scope='session')
def logdir(request):
    return request.config.option.htmlpath.rstrip('report.html')


@fixture(scope='session')
def driver_type(request):
    return request.config.getoption('--driver')


@fixture(scope='session')
def test_type(request):
    return request.config.getoption('--test-type')


@fixture(scope='session')
def cdmi():
    from tests.gui.utils import CDMIClient
    return CDMIClient


@fixture(scope='session')
def onepage():
    from tests.gui.utils import OnePage
    return OnePage


@fixture(scope='session')
def public_onepage():
    from tests.gui.utils import PublicOnePage
    return PublicOnePage


@fixture(scope='session')
def onepanel():
    from tests.gui.utils import Onepanel
    return Onepanel


@fixture(scope='session')
def login_page():
    from tests.gui.utils import LoginPage
    return LoginPage


@fixture(scope='session')
def oz_page():
    from tests.gui.utils import OZLoggedIn
    return OZLoggedIn


@fixture(scope='session')
def op_container():
    from tests.gui.utils import OPLoggedIn
    return OPLoggedIn


@fixture(scope='session')
def public_share():
    from tests.gui.utils import PublicShareView
    return PublicShareView


@fixture(scope='session')
def private_share():
    from tests.gui.utils import PrivateShareView
    return PrivateShareView


@fixture(scope='session')
def privacy_policy():
    from tests.gui.utils import PrivacyPolicy
    return PrivacyPolicy


@fixture(scope='session')
def terms_of_use():
    from tests.gui.utils import TermsOfUse
    return TermsOfUse


@fixture(scope='session')
def data_discovery():
    from tests.gui.utils import DataDiscoveryPage
    return DataDiscoveryPage


@fixture(scope='session')
def modals():
    from tests.gui.utils import Modals
    return Modals


@fixture(scope='session')
def popups():
    from tests.gui.utils import Popups
    return Popups


@fixture
def tmp_memory():
    """Dict to use when one wants to store sth between steps.

    Because of use of multiple browsers, the correct format would be:
     {'browser1': {...}, 'browser2': {...}, ...}
    """
    return defaultdict(dict)


@fixture
def displays():
    """Dict mapping browser to used display (e.g. {'browser1': ':0.0'} )"""
    return {}


@fixture(scope='session')
def clipboard():
    """utility simulating os clipboard"""
    from platform import system as get_system
    from collections import namedtuple
    cls = namedtuple('Clipboard', ['copy', 'paste'])

    def copy(text, display):
        if get_system() == 'Darwin':
            cmd = ['pbcopy']
        else:
            cmd = ['xclip', '-d', display, '-selection', 'c']
        p = sp.Popen(cmd, stdin=sp.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))

    def paste(display):
        if get_system() == 'Darwin':
            cmd = ['pbpaste']
        else:
            cmd = ['xclip', '-d', display, '-selection', 'c', '-o']
        p = sp.Popen(cmd, stdout=sp.PIPE, close_fds=True)
        stdout, _ = p.communicate()
        return stdout.decode('utf-8')

    return cls(copy, paste)


@fixture(scope='session')
def base_url(hosts, maybe_start_env):
    return 'https://{}'.format(hosts['onezone']['hostname'])


@fixture(scope='function', autouse=True)
def _skip_sensitive(request, sensitive_url):
    """Invert the default sensitivity behaviour: consider the test as destructive
    only if it has marker "destructive".
    """
    destructive = 'destructive' in request.node.keywords
    if sensitive_url and destructive:
        skip('This test is destructive and the target URL is '
             'considered a sensitive environment. If this test is '
             'not destructive, add the \'nondestructive\' marker to '
             'it. Sensitive URL: {0}'.format(sensitive_url))


@fixture
def capabilities(request, capabilities, tmpdir):
    """Add --no-sandbox argument for Chrome headless
    Should be the same as adding capability: 'chromeOptions': {'args': ['--no-sandbox'], 'extensions': []}
    """
    if capabilities is None:
        capabilities = {}

    if 'browserName' in capabilities and capabilities['browserName'] == 'chrome' or request.config.option.driver == 'Chrome':
        options = webdriver.ChromeOptions()

        options.binary_location = '/usr/local/bin/google-chrome'

        options.add_argument('--no-sandbox')
        options.add_argument('--enable-popup-blocking')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-infobars')
        options.add_argument('--enable-logging')
        options.add_argument('--v=1')

        options.set_capability('goog:loggingPrefs',
                               {'performance': 'ALL', 'driver': 'ALL', 'browser': 'ALL'})

        options.add_experimental_option("excludeSwitches",
                                        ["enable-automation"])
        prefs = {"download.default_directory": str(tmpdir)}
        options.add_experimental_option("prefs", prefs)
        capabilities.update({'options': options})
    # TODO: use Firefox Marionette driver (geckodriver) for Firefox 47: https://jira.plgrid.pl/jira/browse/VFS-2203
    # but currently this driver is buggy...
    # elif 'browserName' in capabilities and capabilities['browserName'] == 'firefox' or request.config.option.driver == 'Firefox':
        # capabilities['acceptInsecureCerts'] = True
        # capabilities['marionette'] = True

    # currently there are no problems with invalid SSL certs in built-in FF driver and Chrome
    # but some drivers could need it
    # capabilities['loggingPrefs'] = {'browser': 'ALL'}
    # capabilities['acceptSslCerts'] = True

    # uncomment to debug selenium browser init
    # print "DEBUG: Current capabilities: ", capabilities

    return capabilities


# ============================================================================
# Xvfb and ffmpeg options and configurations.
# ============================================================================


@fixture(scope='session')
def screen_width():
    return 1366


@fixture(scope='session')
def screen_height():
    return 1024


@fixture(scope='session')
def screen_depth():
    return 24


@fixture(scope='session')
def screens():
    return [0]


@fixture(scope='session')
def movie_dir(request):
    log_dir = os.path.dirname(request.config.option.htmlpath)
    movie_subdir = os.path.join(log_dir, 'movies')
    if not os.path.exists(movie_subdir):
        os.makedirs(movie_subdir)
    return movie_subdir


@fixture(scope='module')
def xvfb(request, screens, screen_width, screen_height, screen_depth):
    if request.config.getoption('--xvfb'):
        display = xvfb_utils.find_free_display()
        xvfb_proc = xvfb_utils.start_session(display, screens, screen_width,
                                             screen_height, screen_depth)
        try:
            yield [':{}.{}'.format(display, screen) for screen in screens]
        finally:
            xvfb_utils.stop_session(xvfb_proc)
    else:
        yield [os.environ.get('DISPLAY', 'DUMMY_DISPLAY')]


@fixture(scope='function')
def xvfb_recorder(request, xvfb, movie_dir, screen_width, screen_height):
    recording = request.config.getoption('--xvfb-recording')
    mosaic_filter = not request.config.getoption('--no-mosaic-filter')

    if recording != 'none':
        # add timestamp to video name
        file_name = '{}.{}'.format(request.node.name, int(time()))

        # for len(file_name) > 180 ffmpeg is not starting
        file_name = file_name[:180] if len(file_name) > 180 else file_name

        # if there is '/' in file name ffmpeg is not starting
        file_name = file_name.replace('/', '_')

        ffmpeg_proc, movies = start_recording(movie_dir, file_name, xvfb,
                                              screen_width, screen_height,
                                              mosaic_filter)
        request.node._movies = movies

        try:
            yield
        finally:
            stop_recording(ffmpeg_proc)
            # if setup and call of this given passed then whole test passed
            setup_passed = request.node.setup_xvfb_recorder.passed
            call_passed = request.node.call_xvfb_recorder.passed
            if recording == 'failed' and setup_passed and call_passed:
                for movie in movies:
                    try:
                        os.remove(movie)
                    except IOError as ex:
                        if ex.errno not in (errno.ENOENT, errno.ENAMETOOLONG):
                            raise
    else:
        yield


# ============================================================================
# Miscellaneous.
# ============================================================================


@fixture(name='run_unmock')
def run_around_testcase(hosts):
    yield
    unmock_archive_verification('oneprovider-krakow', hosts)

