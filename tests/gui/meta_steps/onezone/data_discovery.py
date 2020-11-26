"""This module contains meta steps for operations on data discovey page in
Onezone using web GUI
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re
import time

import yaml

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.onezone.data_discovery import (
    click_query_button_on_data_disc_page, assert_data_discovery_page)
from tests.gui.steps.onezone.discovery import (
    click_on_option_of_harvester_on_left_sidebar_menu)
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar, click_element_on_lists_on_left_sidebar_menu)
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees only following files in Data '
                  'discovery page:\n{config}'))
@wt(parsers.parse('user of {browser_id} sees only following files on public '
                  'data discovery page:\n{config}'))
@repeat_failed(timeout=WAIT_BACKEND*4, interval=2)
def assert_data_discovery_files(selenium, browser_id, data_discovery, config,
                                spaces):
    click_query_button_on_data_disc_page(selenium, browser_id, data_discovery)
    time.sleep(1)
    assert_files(selenium, browser_id, data_discovery, config, spaces)


def assert_files(selenium, browser_id, data_discovery, config, spaces):
    expected_data = yaml.load(config)
    data_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    _assert_elem_num_equals(expected_data, data_dict)
    for file in expected_data:
        if file == 'spaces':
            _check_spaces_of_data_disc(expected_data['spaces'], data_dict)
        else:
            _assert_data_discovery_files(expected_data[file],
                                         data_dict[file].text, spaces)


def _assert_elem_num_equals(expected_data, data_dict):
    expected_num = len(expected_data)
    spaces = expected_data.get('spaces', [])
    if spaces:
        expected_num = expected_num - 1 + len(spaces)
    assert expected_num == len(data_dict), (f'There should be {expected_num} '
                                            f'files visible but there is '
                                            f'{len(data_dict)}')


def _check_spaces_of_data_disc(expected, actual):
    for space in expected:
        assert space in actual, f'space {space} not harvested'


def _unpack_files_data(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    regex = r'fileName: "(?P<file_name>[^\s]+)"'
    files_data_dict = {}

    for file in data_discovery(driver).results_list:
        files_data_dict[re.findall(regex, file.text)[0]] = file
    return files_data_dict


def _assert_data_discovery_files(expected, actual, spaces):
    for item in expected.items():
        if item[0] == 'spaceId':
            item = ('spaceId', f'"{spaces[item[1]]}"')
        if item[0] == 'xattrs':
            for sub_item in item[1].items():
                if sub_item[0] == 'unexpected':
                    for s_item in sub_item[1].items():
                        _assert_unexpected_xattr(s_item, actual)
                else:
                    _assert_expected_xattr(sub_item, actual)
        else:
            assert (f'{item[0].lower()}: {str(item[1]).lower()}' in
                    actual.lower()), f'{item[0]}: {item[1]} not in {actual}'


def _assert_unexpected_xattr(sub_item, actual):
    regex = f'{sub_item[0]}: {{__value: {sub_item[1]}}}'
    assert regex not in actual, f'{regex} in {actual} but should not be'


def _assert_expected_xattr(sub_item, actual):
    regex = f'{sub_item[0]}: {{__value: {sub_item[1]}}}'
    assert regex in actual, f'{regex} not in {actual}'


@wt(parsers.parse('user of {browser_id} opens Data Discovery page of '
                  '"{harvester_name}" harvester'))
def open_data_discovery_of_harvester(selenium, browser_id, harvester_name,
                                     data_discovery, oz_page):
    option = 'Discovery'
    list_name = 'harvesters'
    option2 = 'data discovery'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, list_name,
                                                harvester_name, oz_page)
    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option2,
                                                      oz_page)
    assert_data_discovery_page(selenium, browser_id, data_discovery)


@wt(parsers.parse('user of {browser_id} clicks on "Go to source file..." for '
                  '"{filename}"'))
def go_to_source_of_file(selenium, browser_id, filename, data_discovery):
    data_dict = _unpack_files_data(selenium, browser_id, data_discovery)
    data_dict[filename].source_button()

