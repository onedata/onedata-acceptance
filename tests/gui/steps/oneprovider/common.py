"""Steps used for common operations in Oneprovider GUI"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time

import yaml
from selenium.common.exceptions import StaleElementReferenceException
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, parse_url
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


def _wait_for_op_session_to_start(selenium, browser_id_list):
    @repeat_failed(timeout=WAIT_BACKEND)
    def _assert_correct_url(d):
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
def g_wait_for_op_session_to_start(selenium, browser_id_list):
    _wait_for_op_session_to_start(selenium, browser_id_list)


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*?) sees that Oneprovider session has started"
    )
)
def wt_wait_for_op_session_to_start(selenium, browser_id_list):
    _wait_for_op_session_to_start(selenium, browser_id_list)


@wt(
    parsers.parse(
        "user of {browser_id} sees that provider name displayed in "
        'Oneprovider page is equal to the name of "{val}" provider'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_provider_name_prov_in_op(selenium, browser_id, val, op_container, hosts):
    val = hosts[val]["name"]
    displayed_name = op_container(selenium[browser_id]).provider_name
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
def wt_assert_provider_name_in_op(selenium, browser_id, val, op_container):
    displayed_name = op_container(selenium[browser_id]).provider_name
    assert displayed_name == val, (
        f"displayed {displayed_name} provider name in Oneprovider GUI instead"
        f" of expected {val}"
    )


@given(
    parsers.parse("possible exception messages appearing for workflow files:\n{config}")
)
def load_exceptions_for_input_files(tmp_memory, config):
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


def _load_exceptions_for_input_files(tmp_memory, config):
    data = yaml.load(config, yaml.Loader)
    for el in data:
        file = list(el.keys())[0]
        exceptions = list(el.values())[0]
        tmp_memory["exceptions"][file] = exceptions


def wait_for_item_to_appear(item):
    for _ in range(50):
        try:
            if item.is_displayed():
                return
            time.sleep(0.1)
        except StaleElementReferenceException:
            time.sleep(0.1)
    raise RuntimeError(f"item {item} did not appear")
