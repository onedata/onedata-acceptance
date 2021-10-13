"""This module contains gherkin steps to run mixed acceptance tests featuring
datasets using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.dataset import *
from tests.gui.steps.oneprovider.browser import (
    assert_status_tag_for_file_in_browser)
from tests.mixed.steps.rest.oneprovider.data import (
    create_dataset_in_op_rest, assert_dataset_for_item_in_op_rest,
    remove_dataset_in_op_rest, assert_write_protection_flag_for_dataset_op_rest,
    check_dataset_structure_in_op_rest)
from tests.mixed.utils.common import NoSuchClientException


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) creates dataset '
               '(?P<option>|with data and metadata write protection flags )for '
               'item "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
               'in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset_in_op(client, user, item_name, space_name, host, tmp_memory,
                         selenium, oz_page, op_container, modals, users, hosts,
                         option):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_dataset(user, tmp_memory, item_name, space_name,
                       selenium, oz_page, op_container, modals, option)
    elif client_lower == 'rest':
        create_dataset_in_op_rest(user, users, hosts, host, space_name,
                                  item_name, option)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) (?P<option>does '
               'not see|sees) dataset for item "(?P<item_name>.*)" in space'
               ' "(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_dataset_for_item_in_op(client, user, item_name, space_name, host,
                                  selenium, oz_page, op_container, tmp_memory,
                                  users, hosts, spaces, option):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_dataset_for_item_in_op_gui(selenium, user, oz_page, space_name,
                                          op_container, tmp_memory, item_name,
                                          option)
    elif client_lower == 'rest':
        assert_dataset_for_item_in_op_rest(user, users, hosts, host, space_name,
                                           item_name, spaces, option)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) removes dataset for item '
               '"(?P<item_name>.*)" in space "(?P<space_name>.*)" '
               'in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_dataset_in_op(client, user, item_name, space_name, host, selenium,
                         oz_page, op_container, tmp_memory, modals, users,
                         hosts, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_dataset_in_op_gui(selenium, user, oz_page, space_name,
                                 op_container, tmp_memory, item_name, modals)
    elif client_lower == 'rest':
        remove_dataset_in_op_rest(user, users, hosts, host, space_name,
                                  item_name, spaces)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) sees(?P<option>.*) write '
               'protection flags? for dataset for item "(?P<item_name>.*)" in'
               ' space "(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_write_protection_flag_for_dataset(client, user, item_name, option,
                                             tmp_memory, users, hosts, host,
                                             space_name, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        data = ' data'
        metadata = ' metadata'
        if data in option:
            status_type = 'data protected'
            assert_status_tag_for_file_in_browser(user, status_type, item_name,
                                                  tmp_memory, which_browser=
                                                  'dataset browser')
        if metadata in option:
            status_type = 'metadata protected'
            assert_status_tag_for_file_in_browser(user, status_type, item_name,
                                                  tmp_memory, which_browser=
                                                  'dataset browser')
    elif client_lower == 'rest':
        assert_write_protection_flag_for_dataset_op_rest(user, users, hosts,
                                                         host, space_name,
                                                         item_name, spaces,
                                                         option)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that datasets '
               'structure in space "(?P<space_name>.*)" in (?P<host>.*) '
               r'is as follow:\n(?P<config>(.|\s)*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_dataset_structure_in_op(client, user, space_name, host, config,
                                  selenium, oz_page, op_container, tmpdir,
                                  tmp_memory, users, hosts, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        check_dataset_structure_in_op_gui(selenium, user, oz_page,
                                          space_name, config, op_container,
                                          tmpdir, tmp_memory)
    elif client_lower == 'rest':
        check_dataset_structure_in_op_rest(user, users, hosts, host, spaces,
                                           space_name, config)
    else:
        raise NoSuchClientException(f'Client: {client} not found')

