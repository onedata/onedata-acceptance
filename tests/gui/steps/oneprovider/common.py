"""Steps used for common operations in Oneprovider GUI"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import os
import time
from os import PathLike

import yaml
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND, WAIT_NORMAL_DOWNLOAD
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import OPLoggedIn
from tests.gui.utils.generic import parse_seq, parse_url
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


def _wait_for_op_session_to_start(
    selenium: SeleniumDrivers, browser_id_list: str
) -> None:
    @repeat_failed(timeout=WAIT_BACKEND)
    def _assert_correct_url(d: WebDriver) -> None:
        try:
            found = parse_url(d.current_url).group("where")
        except AttributeError as exc:
            raise RuntimeError("no access part found in url") from exc
        if "opw" != found.lower():
            raise RuntimeError(
                f"expected opw as access part in url instead got: {found}"
            )

    time.sleep(12)
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]

        _assert_correct_url(driver)


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.*?) seen that Oneprovider session has started"
    )
)
def g_wait_for_op_session_to_start(
    selenium: SeleniumDrivers, browser_id_list: str
) -> None:
    _wait_for_op_session_to_start(selenium, browser_id_list)


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*?) sees that Oneprovider session has started"
    )
)
def wt_wait_for_op_session_to_start(
    selenium: SeleniumDrivers, browser_id_list: str
) -> None:
    _wait_for_op_session_to_start(selenium, browser_id_list)


@wt(
    parsers.parse(
        "user of {browser_id} sees that provider name displayed in "
        'Oneprovider page is equal to the name of "{val}" provider'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_provider_name_prov_in_op(
    selenium: SeleniumDrivers, browser_id: str, val: str, hosts: Hosts
) -> None:
    val = hosts[val]["name"]
    displayed_name = OPLoggedIn(selenium[browser_id]).provider_name
    assert displayed_name == val, (
        f"displayed {displayed_name} provider name in Oneprovider GUI "
        f"instead of expected {val}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that provider name displayed in "
        'Oneprovider page is equal to "{val}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_provider_name_in_op(
    selenium: SeleniumDrivers, browser_id: str, val: str
) -> None:
    displayed_name = OPLoggedIn(selenium[browser_id]).provider_name
    assert displayed_name == val, (
        f"displayed {displayed_name} provider name in Oneprovider GUI instead"
        f" of expected {val}"
    )


@given(
    parsers.parse("possible exception messages appearing for workflow files:\n{config}")
)
def load_exceptions_for_input_files(tmp_memory: TmpMemory, config: str) -> None:
    """
    Configuration is as follows
    - file_name:
        - exception1
        - exception2
        ...
    - file_name2:
    ...
    """

    _load_exceptions_for_input_files(tmp_memory, config)


def _load_exceptions_for_input_files(tmp_memory: TmpMemory, config: str) -> None:
    data = yaml.load(config, yaml.Loader)
    for el in data:
        file = list(el.keys())[0]
        exceptions = list(el.values())[0]
        tmp_memory["exceptions"][file] = exceptions


def wait_for_item_to_appear(item: WebElement) -> None:
    for _ in range(50):
        try:
            if item.is_displayed():
                return
            time.sleep(0.1)
        except StaleElementReferenceException:
            time.sleep(0.1)
    raise RuntimeError(f"item {item} did not appear")


@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_item_to_disappear(item: WebElement) -> None:
    try:
        item.is_displayed()
        raise AssertionError("Element is visible")
    except StaleElementReferenceException:
        pass


@repeat_failed(timeout=WAIT_NORMAL_DOWNLOAD)
def wait_for_file_with_unknown_name_to_download(
    n_files_before_download: int, dir_path: str | PathLike[str]
) -> None:
    # wait for a file to download, we don`t know the name of the file
    # so there is a way we can check that file was downloaded
    n_files_after_download = len(os.listdir(dir_path))
    assert n_files_after_download > n_files_before_download, "Downloading did not start"
    file_name = os.listdir(dir_path)[-1]
    assert_file_download_finished(file_name)


def assert_file_download_finished(file_name: str) -> None:
    _, ext = os.path.splitext(file_name)
    assert ext != ".crdownload", f"Downloading file {file_name} did not finish"
