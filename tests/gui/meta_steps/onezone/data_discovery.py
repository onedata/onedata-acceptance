"""This module contains meta steps for operations on data discovey page in
Onezone using web GUI
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from functools import partial
from typing import cast

import yaml

from tests.gui.steps.onezone.harvesters.data_discovery import (
    wait_for_data_discovery_query_result,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import DataDiscoveryPage as DataDiscovery
from tests.gui.utils.onezone.data_discovery_page import ResultSample
from tests.type_definitions import JsonObject, JsonValue, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


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
def assert_data_discovery_files(
    selenium: SeleniumDrivers, browser_id: str, config: str, spaces: dict[str, str]
) -> None:
    wait_for_data_discovery_query_result(
        selenium,
        browser_id,
        partial(
            assert_files,
            selenium=selenium,
            browser_id=browser_id,
            config=config,
            spaces=spaces,
        ),
    )


def assert_files(
    selenium: SeleniumDrivers, browser_id: str, config: str, spaces: dict[str, str]
) -> None:
    expected_data = yaml.load(config, yaml.Loader)
    data_dict = _unpack_files_data(selenium, browser_id)
    _assert_elem_num_equals(expected_data, data_dict)
    for file in expected_data:
        if file == "spaces":
            _check_spaces_of_data_disc(expected_data["spaces"], data_dict)
        else:
            _assert_data_discovery_files(
                expected_data[file], data_dict[file].text, spaces
            )


def _assert_elem_num_equals(
    expected_data: JsonObject, data_dict: dict[str, ResultSample]
) -> None:
    expected_num = len(expected_data)
    spaces = cast(list[str], expected_data.get("spaces", []))
    if spaces:
        expected_num = expected_num - 1 + len(spaces)
    assert expected_num == len(
        data_dict
    ), f"There should be {expected_num} files visible but there is {len(data_dict)}"


def _check_spaces_of_data_disc(
    expected: list[str], actual: dict[str, ResultSample]
) -> None:
    for space in expected:
        assert space in actual, f"space {space} not harvested"


def _unpack_files_data(
    selenium: SeleniumDrivers, browser_id: str
) -> dict[str, ResultSample]:
    driver = selenium[browser_id]
    regex = r'fileName: "(?P<file_name>[^\s]+)"'
    files_data_dict = {}

    for file in DataDiscovery(driver).results_list:
        files_data_dict[re.findall(regex, file.text)[0]] = file
    return files_data_dict


def _assert_data_discovery_files(
    expected: JsonObject, actual: str, spaces: dict[str, str]
) -> None:
    for item in expected.items():
        if item[0] == "spaceId":
            item = ("spaceId", f'"{spaces[cast(str, item[1])]}"')
        if item[0] == "xattrs":
            xattrs = cast(dict[str, JsonObject], item[1])
            for sub_item in xattrs.items():
                if sub_item[0] == "unexpected":
                    for s_item in sub_item[1].items():
                        _assert_unexpected_xattr(s_item, actual)
                else:
                    _assert_expected_xattr(sub_item, actual)
        else:
            assert (
                f"{item[0].lower()}: {str(item[1]).lower()}" in actual.lower()
            ), f"{item[0]}: {item[1]} not in {actual}"


def _assert_unexpected_xattr(sub_item: tuple[str, JsonValue], actual: str) -> None:
    regex = f"{sub_item[0]}: {{__value: {sub_item[1]}}}"
    assert regex not in actual, f"{regex} in {actual} but should not be"


def _assert_expected_xattr(sub_item: tuple[str, JsonValue], actual: str) -> None:
    regex = f"{sub_item[0]}: {{__value: {sub_item[1]}}}"
    assert regex in actual, f"{regex} not in {actual}"


def _assert_unexpected_properties_of_files(
    unexpected: JsonObject, actual: str, spaces: dict[str, str]
) -> None:
    for item in unexpected.items():
        if item[0] == "spaceId":
            item = ("spaceId", f'"{spaces[cast(str, item[1])]}"')
        if item[0] == "xattrs":
            for sub_item in cast(JsonObject, item[1]).items():
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
def assert_not_files_properties(
    selenium: SeleniumDrivers, browser_id: str, config: str, spaces: dict[str, str]
) -> None:
    unexpected_data = yaml.load(config, yaml.Loader)
    data_dict = _unpack_files_data(selenium, browser_id)
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
def see_files_with_order(
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    files_list = yaml.load(config, yaml.Loader)
    data_dict = _unpack_files_data(selenium, browser_id)
    assert len(files_list) == len(data_dict)
    for pair in zip(files_list, data_dict):
        assert pair[0] == pair[1], "Files are not in order"


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Go to source file..." for "{filename}"'
    )
)
def go_to_source_of_file(
    selenium: SeleniumDrivers, browser_id: str, filename: str
) -> None:
    data_dict = _unpack_files_data(selenium, browser_id)
    data_dict[filename].source_button()


@wt(parsers.parse("user of {browser_id} sees {number} files on data discovery page"))
def assert_number_of_files_on_data_disc(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    files_dict = _unpack_files_data(selenium, browser_id)
    assert len(files_dict) == int(
        number
    ), f"Expected: {number} files but only {len(files_dict)} given"


@wt(
    parsers.parse(
        "user of {browser_id} chooses following properties to "
        "filter on data discovery page:\n{config}"
    )
)
def choose_properties_to_filter(
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    data = yaml.load(config, yaml.Loader)
    _parse_data(data, selenium, browser_id)


def _parse_data(
    data: list[JsonValue], selenium: SeleniumDrivers, browser_id: str
) -> None:
    page = DataDiscovery(selenium[browser_id])
    for item in data:
        if isinstance(item, dict):
            if [*item][0] == "__onedata":
                page.filter_properties_tree.tree_nodes["__onedata"].expander()
                attributes = cast(list[JsonValue], item["__onedata"])
                for attribute in attributes:
                    if isinstance(attribute, dict):
                        if [*attribute][0] == "xattrs":
                            node = page.filter_properties_tree.tree_nodes[
                                "__onedata"
                            ].onedata_tree_nodes["xattrs"]
                            node.expander()
                            nodes = node.xattrs_tree_nodes
                            for property_name in cast(list[str], attribute["xattrs"]):
                                nodes[property_name].checkbox.click()
                        else:
                            raise ValueError(f"Do not support {attribute}")
                    else:
                        nodes = page.filter_properties_tree.tree_nodes[
                            "__onedata"
                        ].onedata_tree_nodes
                        nodes[attribute].checkbox.click()
            else:
                raise ValueError(f"Do not support {item}")
        else:
            page.filter_properties_tree.tree_nodes[item].checkbox.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that querying curl result matches "
        "following files:\n{config}"
    )
)
def compare_files_with_curl(
    browser_id: str, tmp_memory: TmpMemory, config: str
) -> None:
    curl_res = tmp_memory[browser_id]["curl result"]
    expected_data = yaml.load(config, yaml.Loader)

    query_curl_data = curl_res["hits"]["hits"]
    curl_dict = _curl_data_to_dict(query_curl_data)

    msg = "curl and expected data does not match"

    assert len(expected_data) == len(curl_dict), msg

    for file_name in expected_data:
        for property_name in expected_data[file_name]:
            if property_name == "xattrs":
                xattrs = expected_data[file_name][property_name]
                for xattr in xattrs:
                    onedata = cast(JsonObject, curl_dict[file_name]["__onedata"])
                    file_xattrs = cast(dict[str, JsonObject], onedata["xattrs"])
                    assert file_xattrs[xattr]["__value"] == xattrs[xattr], msg

            else:
                assert (
                    expected_data[file_name][property_name]
                    == curl_dict[file_name][property_name]
                ), msg


def _curl_data_to_dict(
    query_curl_data: list[JsonObject],
) -> dict[str, JsonObject]:
    new_dict = {}
    for entry in query_curl_data:
        source = cast(JsonObject, entry["_source"])
        onedata = cast(JsonObject, source["__onedata"])
        file_name = cast(str, onedata["fileName"])
        new_dict[file_name] = source
    return new_dict
