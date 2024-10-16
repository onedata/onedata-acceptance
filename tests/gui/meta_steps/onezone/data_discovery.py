"""This module contains meta steps for operations on data discovey page in
Onezone using web GUI
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time

import yaml
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.onezone.harvesters.data_discovery import (
    assert_data_discovery_page,
    click_button_on_data_disc_page,
)
from tests.gui.steps.onezone.harvesters.discovery import (
    click_on_option_of_harvester_on_left_sidebar_menu,
)
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_in_the_sidebar,
)
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} sees only following files in Data "
        "discovery page:\n{config}"
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees only following files on public "
        "data discovery page:\n{config}"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4, interval=2)
def assert_data_discovery_files(selenium, browser_id, data_discovery, config, spaces):
    button_name = "Query"

    click_button_on_data_disc_page(selenium, browser_id, data_discovery, button_name)
    time.sleep(1)
    assert_files(selenium, browser_id, data_discovery, config, spaces)


def assert_files(selenium, browser_id, data_discovery, config, spaces):
    expected_data = yaml.load(config, yaml.Loader)
    data_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    _assert_elem_num_equals(expected_data, data_dict)
    for file in expected_data:
        if file == "spaces":
            _check_spaces_of_data_disc(expected_data["spaces"], data_dict)
        else:
            _assert_data_discovery_files(
                expected_data[file], data_dict[file].text, spaces
            )


def _assert_elem_num_equals(expected_data, data_dict):
    expected_num = len(expected_data)
    spaces = expected_data.get("spaces", [])
    if spaces:
        expected_num = expected_num - 1 + len(spaces)
    assert expected_num == len(
        data_dict
    ), f"There should be {expected_num} files visible but there is {len(data_dict)}"


def _check_spaces_of_data_disc(expected, actual):
    for space in expected:
        assert space in actual, f"space {space} not harvested"


def _unpack_files_data(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    regex = r'fileName: "(?P<file_name>[^\s]+)"'
    files_data_dict = {}

    for file in data_discovery(driver).results_list:
        files_data_dict[re.findall(regex, file.text)[0]] = file
    return files_data_dict


def _assert_data_discovery_files(expected, actual, spaces):
    for item in expected.items():
        if item[0] == "spaceId":
            item = ("spaceId", f'"{spaces[item[1]]}"')
        if item[0] == "xattrs":
            for sub_item in item[1].items():
                if sub_item[0] == "unexpected":
                    for s_item in sub_item[1].items():
                        _assert_unexpected_xattr(s_item, actual)
                else:
                    _assert_expected_xattr(sub_item, actual)
        else:
            assert (
                f"{item[0].lower()}: {str(item[1]).lower()}" in actual.lower()
            ), f"{item[0]}: {item[1]} not in {actual}"


def _assert_unexpected_xattr(sub_item, actual):
    regex = f"{sub_item[0]}: {{__value: {sub_item[1]}}}"
    assert regex not in actual, f"{regex} in {actual} but should not be"


def _assert_expected_xattr(sub_item, actual):
    regex = f"{sub_item[0]}: {{__value: {sub_item[1]}}}"
    assert regex in actual, f"{regex} not in {actual}"


def _assert_unexpected_properties_of_files(unexpected, actual, spaces):
    for item in unexpected.items():
        if item[0] == "spaceId":
            item = ("spaceId", f'"{spaces[item[1]]}"')
        if item[0] == "xattrs":
            for sub_item in item[1].items():
                _assert_unexpected_xattr(sub_item, actual)
        else:
            assert not (
                f"{item[0].lower()}: {str(item[1]).lower()}" in actual.lower()
            ), f"{item[0]}: {item[1]} in {actual}"


@wt(
    parsers.parse(
        "user of {browser_id} does not see following properties of "
        "files in data discovery page:\n{config}"
    )
)
def assert_not_files_properties(selenium, browser_id, data_discovery, config, spaces):
    unexpected_data = yaml.load(config, yaml.Loader)
    data_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    for file in unexpected_data:
        _assert_unexpected_properties_of_files(
            unexpected_data[file], data_dict[file].text, spaces
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees files with following order on "
        "data discovery page:\n{config}"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def see_files_with_order(selenium, browser_id, data_discovery, config):
    files_list = yaml.load(config, yaml.Loader)
    data_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    assert len(files_list) == len(data_dict)
    for pair in zip(files_list, data_dict):
        assert pair[0] == pair[1], "Files are not in order"


@wt(
    parsers.parse(
        'user of {browser_id} opens Data Discovery page of "{harvester_name}" harvester'
    )
)
def open_data_discovery_of_harvester(
    selenium, browser_id, harvester_name, data_discovery, oz_page
):
    option = "Discovery"
    list_name = "harvesters"
    option2 = "data discovery"

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, list_name, harvester_name, oz_page
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option2, oz_page
    )
    assert_data_discovery_page(selenium, browser_id, data_discovery)


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Go to source file..." for "{filename}"'
    )
)
def go_to_source_of_file(selenium, browser_id, filename, data_discovery):
    data_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    data_dict[filename].source_button()


@wt(parsers.parse("user of {browser_id} sees {number} files on data discovery page"))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_of_files_on_data_disc(
    selenium, browser_id, data_discovery, number: int
):
    files_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    assert (
        len(files_dict) == number
    ), f"Expected: {number} files but only {len(files_dict)} given"


@wt(
    parsers.parse(
        "user of {browser_id} chooses following properties to "
        "filter on data discovery page:\n{config}"
    )
)
def choose_properties_to_filter(selenium, browser_id, config, data_discovery):
    data = yaml.load(config, yaml.Loader)
    _parse_data(data, data_discovery, selenium, browser_id)


def _parse_data(data, data_discovery, selenium, browser_id):
    page = data_discovery(selenium[browser_id])
    for item in data:
        if isinstance(item, dict):
            if [*item][0] == "__onedata":
                page.filter_properties_tree.tree_nodes["__onedata"].expander()
                attrs = item["__onedata"]
                for attr in attrs:
                    if isinstance(attr, dict):
                        if [*attr][0] == "xattrs":
                            node = page.filter_properties_tree.tree_nodes[
                                "__onedata"
                            ].onedata_tree_nodes["xattrs"]
                            node.expander()
                            nodes = node.xattrs_tree_nodes
                            for prop in attr["xattrs"]:
                                nodes[prop].checkbox.click()
                        else:
                            raise RuntimeError(f"Do not support {attr}")
                    else:
                        nodes = page.filter_properties_tree.tree_nodes[
                            "__onedata"
                        ].onedata_tree_nodes
                        nodes[attr].checkbox.click()
            else:
                raise RuntimeError(f"Do not support {item}")
        else:
            page.filter_properties_tree.tree_nodes[item].checkbox.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that querying curl result matches "
        "following files:\n{config}"
    )
)
def compare_files_with_curl(browser_id, tmp_memory, config):
    curl_res = tmp_memory[browser_id]["curl result"]
    expected_data = yaml.load(config, yaml.Loader)

    query_curl_data = curl_res["hits"]["hits"]
    curl_dict = _curl_data_to_dict(query_curl_data)

    msg = "curl and expected data does not match"

    assert len(expected_data) == len(curl_dict), msg

    for file_name in expected_data:
        for prop in expected_data[file_name]:
            if prop == "xattrs":
                xattrs = expected_data[file_name][prop]
                for xattr in xattrs:
                    file_xattrs = curl_dict[file_name]["__onedata"]["xattrs"]
                    assert file_xattrs[xattr]["__value"] == xattrs[xattr], msg

            else:
                assert expected_data[file_name][prop] == curl_dict[file_name][prop], msg


def _curl_data_to_dict(query_curl_data):
    new_dict = {}
    for entry in query_curl_data:
        file_name = entry["_source"]["__onedata"]["fileName"]
        new_dict[file_name] = entry["_source"]
    return new_dict
