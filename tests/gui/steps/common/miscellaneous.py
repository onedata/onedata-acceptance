"""This module contains gherkin steps to run acceptance tests in web GUI."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import os
import subprocess
from typing import Optional

import yaml
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as Wait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import Onepanel, Popups
from tests.gui.utils.generic import transform
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.entities_setup import (
    DOWNLOAD_INACTIVITY_PERIOD_SEC,
    GUI_DOWNLOAD_CHUNK_SIZE,
)
from tests.utils.utils import repeat_failed


@repeat_failed(attempts=WAIT_FRONTEND)
def _enter_text(input_box: WebElement, text: str) -> None:
    input_box.clear()
    input_box.send_keys(text)
    if input_box.get_attribute("value") != text and input_box.text != text:
        raise RuntimeError(f'entering "{text}" to input box failed')


@wt(parsers.parse('user of {browser_id} types "{text}" on keyboard'))
def type_string_into_active_element(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    _enter_text(selenium[browser_id].switch_to.active_element, text)


@wt(parsers.parse("user of {browser_id} types received {item_type} on keyboard"))
def type_item_into_active_element(
    selenium: SeleniumDrivers, browser_id: str, item_type: str, tmp_memory: TmpMemory
) -> None:
    item = tmp_memory[browser_id]["mailbox"][item_type]
    _enter_text(selenium[browser_id].switch_to.active_element, item)


@wt(parsers.parse("user of {browser_id} presses enter on keyboard"))
def press_enter_on_active_element(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse("user of {browser_id} presses tab on keyboard"))
def press_tab_on_active_element(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.TAB)


@wt(parsers.parse("user of {browser_id} presses backspace on keyboard"))
def press_backspace_on_active_element(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.BACKSPACE)


def assert_title_contains(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page_title = selenium[browser_id].title
    assert text in page_title, f"{page_title} page title should contain {text}"


@wt(
    parsers.parse(
        'user of {browser_id} should see that the page title contains "{text}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_title_contains(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    assert_title_contains(selenium, browser_id, text)


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*) clicks on "
        '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_popup(
    selenium: SeleniumDrivers, browser_id: str, btn: str, popup: str
) -> None:
    getattr(Popups(selenium[browser_id]), transform(popup)).buttons[btn].click()


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.*) clicked on "
        '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def g_click_on_btn_in_popup(
    selenium: SeleniumDrivers, browser_id: str, btn: str, popup: str
) -> None:
    getattr(Popups(selenium[browser_id]), transform(popup)).buttons[btn].click()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option in menu popup'))
def click_option_in_popup_labeled_menu(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    Popups(driver).menu_popup_with_label.menu[option]()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option in menu'))
def click_option_in_popup_text_menu(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    Popups(driver).menu_popup_with_text.menu[option]()


@wt(parsers.re("pass"))
def pass_test() -> None:
    pass


@wt(
    parsers.parse(
        "user of {browser_id} waits until scanning is finished "
        "in storage import tab in Onepanel"
    )
)
def wait_until_scanning_is_finished_in_storage_import_tab(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Wait(
        driver,
        timeout=WAIT_BACKEND * 2,
        ignored_exceptions=[RuntimeError],
    ).until(
        lambda driver: Onepanel(
            driver
        ).content.spaces.space.sync_chart.start_scan_is_green(),
        message="Waiting for start scan button to be available failed",
    )


@repeat_failed(interval=1, timeout=90, exceptions=NoSuchElementException)
def switch_to_iframe(
    selenium: SeleniumDrivers, browser_id: str, _selector: Optional[str] = None
) -> None:
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)


@wt(
    parsers.parse(
        "user of {browser_id} sets copied {elem} as {var_name} environment variable"
    )
)
def set_env_variable_with_copied_val(
    clipboard: Clipboard, var_name: str, displays: dict[str, str], browser_id: str
) -> None:
    var_value = clipboard.paste(display=displays[browser_id])
    _set_env_variable(var_name, var_value)


def _set_env_variable(var_name: str, var_value: str) -> None:
    os.environ[var_name] = var_value


@wt(parsers.parse("user of {browser_id} runs curl command copied from {page} page"))
def run_curl_command(
    clipboard: Clipboard,
    displays: dict[str, str],
    browser_id: str,
    tmp_memory: TmpMemory,
    page: str,
) -> None:
    curl_cmd = clipboard.paste(display=displays[browser_id])

    # -k option avoids certificate check
    curl_cmd = curl_cmd + " -k"
    status, output = subprocess.getstatusoutput(curl_cmd)
    assert status == 0, "CURL command did not succeeded"
    json_data = _process_curl_output(output, page)
    tmp_memory[browser_id]["curl result"] = json_data


def _process_curl_data_discovery_output(output: str) -> dict[str, object]:
    output = output.replace('\\"', '"')
    output_lines = output.split("\n")
    output_json = output_lines[-1].split('"body"')[-1]
    output_json = output_json.lstrip(':"')
    output_json = output_json.rstrip('"}')
    output_json = output_json + "}}"

    return json.loads(output_json)


def _process_onedata_curl_output(output: str) -> dict[str, object]:
    output_lines = output.split("\n")
    output_json = output_lines[-1]

    return json.loads(output_json)


def _process_curl_output(output: str, page: str) -> dict[str, object]:
    if page == "data discovery":
        return _process_curl_data_discovery_output(output)
    return _process_onedata_curl_output(output)


@wt(
    parsers.parse(
        "user of {browser_id} sees that curl result matches following config:\n{config}"
    )
)
def assert_curl_result_with_config(
    browser_id: str, tmp_memory: TmpMemory, config: str
) -> None:
    curl_res = tmp_memory[browser_id]["curl result"]
    expected_data = yaml.load(config, yaml.Loader)

    for key, val in expected_data.items():
        assert (
            curl_res[_camel_transform(key)] == val
        ), f"{key}: {val} not in curl result"


def _camel_transform(phrase: str) -> str:
    output = phrase.title().replace(" ", "")
    return output[0].lower() + output[1:]


def network_throttling_download(driver: WebDriver) -> None:
    download_kb = (GUI_DOWNLOAD_CHUNK_SIZE / DOWNLOAD_INACTIVITY_PERIOD_SEC) * 1024

    driver.set_network_conditions(
        latency=5,
        download_throughput=float(download_kb) / 8 * 1024,
        upload_throughput=500 * 1024,
    )
