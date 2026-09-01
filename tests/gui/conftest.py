"""
Define fixtures used in web GUI acceptance/behavioral tests.
"""

__author__ = "Jakub Liput, Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
# pylint: disable=unused-import

import os
import re
import subprocess as sp
from collections import defaultdict
from typing import Generator, cast

import pytest
from _pytest._py.path import LocalPath
from _pytest.config.argparsing import Parser
from _pytest.reports import TestReport
from pytest import fixture, hookimpl, skip
from pytest_bdd.parser import Feature, Scenario, Step
from selenium import webdriver

from tests import LOGDIRS
from tests.conftest import export_logs, get_log_dir_path
from tests.gui.sse_fixtures import (
    async_loop_in_thread,
    monitors,
    space_files_monitor_factory,
)
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.common.constants import (
    DRIVER_CREATION_RETRIES,
    RESPONSIVE_LAYOUT_DELAY,
    SCREEN_PARAMETERS,
    SELENIUM_IMPLICIT_WAIT,
    WAIT_BACKEND,
    WAIT_EXTENDED_UPLOAD,
    WAIT_EXTENDED_WORKFLOW_EXECUTION,
    WAIT_FRONTEND,
    WAIT_NORMAL_DOWNLOAD,
    WAIT_NORMAL_UPLOAD,
    WAIT_NORMAL_WORKFLOW_EXECUTION,
    WAIT_PODS_TERMINATION,
)
from tests.oneclient.steps.environment_steps import unmock_archive_verification
from tests.type_definitions import (
    HookOutcome,
    Hosts,
    JsonObject,
)
from tests.utils import onenv_utils, xvfb_utils
from tests.utils.ffmpeg_utils import RecorderManager
from tests.utils.path_utils import build_test_dir_name, make_logdir

# ============================================================================
# PYTEST CONFIGURATION
# =============================================================================


def pytest_configure(config: pytest.Config) -> None:
    """Set default path for Selenium HTML report if explicit '--html=' not specified"""
    htmlpath = config.option.htmlpath
    if htmlpath is None:
        _test_type = config.option.test_type
        _logdir = make_logdir(LOGDIRS.get(_test_type), "report")
        config.option.htmlpath = os.path.join(_logdir, "report.html")


def pytest_addoption(parser: Parser) -> None:
    selenium_group = parser.getgroup("selenium", "selenium")
    selenium_group.addoption("--xvfb", action="store_true", help="run Xvfb for tests")
    selenium_group.addoption(
        "--no-mosaic-filter",
        action="store_true",
        help="turn off mosaic filter if recording tests with multiple browsers",
    )


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item) -> Generator[None, HookOutcome, None]:
    outcome = yield
    rep = cast(TestReport, outcome.get_result())
    setattr(item, rep.when + "_xvfb_recorder", rep)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        item.name = re.sub("{.*}", "", item.name)
        item.name = re.sub("<.*>", "", item.name)


def pytest_bdd_before_scenario(
    request: pytest.FixtureRequest,
    feature: Feature,
    scenario: Scenario,
) -> None:
    RecorderManager(request).handle_start_recording(SCREEN_PARAMETERS)
    print("\n" + "=" * 65)
    print(f"- Executing scenario '{scenario.name}'")
    print(f"- from feature '{feature.name}'")
    print("-" * 65)


def pytest_bdd_before_step_call(step: Step) -> None:
    print(f"-- Executing step: {format_step_name(step)}")


def pytest_bdd_after_scenario(request: pytest.FixtureRequest) -> None:
    logdir_path = get_log_dir_path(request)
    lambda_log_dir_name = build_test_dir_name(request.node)
    onenv_utils.run_onenv_command(
        "export",
        [
            logdir_path,
            "--lambda-logs-only",
            "--lambda-logs-dir",
            lambda_log_dir_name,
        ],
        fail_with_error=True,
    )
    onenv_utils.run_onenv_command(
        "clean",
        ["--lambda-pods-only"],
        fail_with_error=True,
    )

    print("=================================================================")


def pytest_bdd_step_error(step: Step, exception: BaseException) -> None:
    print(f"--- STEP FAILED on {step}")
    print(f"--- Exception: {exception}\n")


def format_step_name(step: Step) -> str:
    step_name = step.name.split("\n")
    if len(step_name) > 1:
        return step_name[0] + " (...)"
    return step_name[0]


# =============================================================================
# PYTEST FIXTURES
# =============================================================================


@fixture(autouse=True, scope="module")
def finalize(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    yield
    export_logs(request)


@fixture(scope="session")
def logdir(request: pytest.FixtureRequest) -> str:
    return request.config.option.htmlpath.rstrip("report.html")


@fixture(scope="session")
def driver_type(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--driver")


@fixture(scope="session")
def test_type(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--test-type")


@fixture
def tmp_memory() -> TmpMemory:
    """Dict to use when one wants to store sth between steps.

    Because of use of multiple browsers, the correct format would be:
     {'browser1': {...}, 'browser2': {...}, ...}
    """
    return cast(TmpMemory, defaultdict(dict))


@fixture
def displays() -> dict[str, str]:
    """Dict mapping browser to used display (e.g. {'browser1': ':0.0'} )"""
    return {}


@fixture(scope="session")
def clipboard() -> Clipboard:
    """utility simulating os clipboard"""
    from collections import namedtuple
    from platform import system as get_system

    def copy(text: str, display: str) -> None:
        if get_system() == "Darwin":
            cmd = ["pbcopy"]
        else:
            cmd = ["xclip", "-d", display, "-selection", "c"]
        with sp.Popen(cmd, stdin=sp.PIPE, close_fds=True) as p:
            p.communicate(input=text.encode("utf-8"))

    def paste(display: str) -> str:
        if get_system() == "Darwin":
            cmd = ["pbpaste"]
        else:
            cmd = ["xclip", "-d", display, "-selection", "c", "-o"]
        with sp.Popen(cmd, stdout=sp.PIPE, close_fds=True) as p:
            stdout, _ = p.communicate()
        return stdout.decode("utf-8")

    return Clipboard(copy, paste)


@fixture(scope="session")
def base_url(hosts: Hosts, maybe_start_env: object) -> str:
    return f'https://{hosts["onezone"]["hostname"]}'


@fixture(scope="function", autouse=True)
def _skip_sensitive(request: pytest.FixtureRequest, sensitive_url: object) -> None:
    """Invert the default sensitivity behaviour: consider the test as destructive
    only if it has marker "destructive".
    """
    destructive = "destructive" in request.node.keywords
    if sensitive_url and destructive:
        skip(
            "This test is destructive and the target URL is "
            "considered a sensitive environment. If this test is "
            "not destructive, add the 'nondestructive' marker to "
            f"it. Sensitive URL: {sensitive_url}"
        )


@fixture
def capabilities(
    request: pytest.FixtureRequest,
    capabilities: JsonObject,
    tmpdir: LocalPath,
) -> JsonObject:
    """Add --no-sandbox argument for Chrome headless
    Should be the same as adding
    capability: 'chromeOptions': {'args': ['--no-sandbox'], 'extensions': []}
    """
    if capabilities is None:
        capabilities = {}

    if (
        "browserName" in capabilities
        and capabilities["browserName"] == "chrome"
        or request.config.option.driver == "Chrome"
    ):
        options = webdriver.ChromeOptions()

        options.binary_location = "/usr/local/bin/google-chrome"

        options.add_argument("--no-sandbox")
        options.add_argument("--enable-popup-blocking")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-infobars")
        options.add_argument("--enable-logging")
        options.add_argument("--v=1")
        # Chrome may crash in Docker containers on certain pages due to
        # too small /dev/shm. So you may have to fix the small /dev/shm size.
        # Another way to make it work would be to add the chrome_options
        # as --disable-dev-shm-usage. This will force Chrome to use
        # the /tmp directory instead. This may slow down the execution
        # since disk will be used instead of memory.
        options.add_argument("--disable-dev-shm-usage")

        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL", "driver": "ALL", "browser": "ALL"},
        )

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        prefs = {"download.default_directory": str(tmpdir)}
        options.add_experimental_option("prefs", prefs)
        capabilities.update({"options": options})
    # TODO: VFS-2203 use Firefox Marionette driver (geckodriver)
    #  for Firefox 47: https://jira.plgrid.pl/jira/browse/VFS-2203
    # but currently this driver is buggy...
    # elif 'browserName' in capabilities and capabilities['browserName'] == /
    # 'firefox' or request.config.option.driver == 'Firefox':
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


@fixture(scope="session")
def screens() -> list[int]:
    return [0]


@fixture(scope="session")
def movie_dir(request: pytest.FixtureRequest) -> str:
    log_dir = os.path.dirname(request.config.option.htmlpath)
    movie_subdir = os.path.join(log_dir, "movies")
    if not os.path.exists(movie_subdir):
        os.makedirs(movie_subdir)
    return movie_subdir


@fixture(scope="module")
def xvfb(
    request: pytest.FixtureRequest,
    screens: list[int],
) -> Generator[list[str], None, None]:
    if request.config.getoption("--xvfb"):
        display = xvfb_utils.find_free_display()
        xvfb_proc = xvfb_utils.start_session(
            display,
            screens,
            SCREEN_PARAMETERS["width"],
            SCREEN_PARAMETERS["height"],
            SCREEN_PARAMETERS["depth"],
        )
        try:
            yield [f":{display}.{screen}" for screen in screens]
        finally:
            xvfb_utils.stop_session(xvfb_proc)
    else:
        yield [os.environ.get("DISPLAY", "DUMMY_DISPLAY")]


@fixture(scope="session")
def should_record() -> bool:
    return True


# ============================================================================
# Miscellaneous.
# ============================================================================


@fixture(name="run_unmock")
def run_around_testcase(hosts: Hosts) -> Generator[None, None, None]:
    yield
    unmock_archive_verification("oneprovider-krakow", hosts)
