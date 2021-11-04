"""This module contains gherkin steps to run mixed acceptance tests featuring
archives using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.archives import *
from tests.mixed.steps.rest.oneprovider.data import (
    create_archive_in_op_rest, assert_archive_in_op_rest,
    remove_archive_in_op_rest, assert_bagit_archive_in_op_rest)
from tests.mixed.utils.common import NoSuchClientException


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) creates archive for '
               'item "(?P<item_name>.*)" in space "(?P<space_name>.*)"'
               ' in (?P<host>.*) with following '
               r'configuration:\n(?P<config>(.|\s)*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive_in_op(client, user, item_name, space_name, host, tmp_memory,
                         selenium, oz_page, op_container, modals, users, hosts,
                         config, spaces, clipboard, displays):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_archive(user, selenium, config, item_name, space_name,
                       oz_page, op_container, tmp_memory, modals,
                       clipboard, displays)
    elif client_lower == 'rest':
        create_archive_in_op_rest(user, users, hosts, host, space_name,
                                  item_name, config, spaces, tmp_memory)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) (?P<option>does not '
               'see|sees) archive with description: "(?P<description>.*)" for'
               ' item "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
               'in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_in_op(client, user, item_name, space_name, host, tmp_memory,
                         selenium, oz_page, op_container, users, hosts,
                         spaces, option, description):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_archive_in_op_gui(user, selenium, item_name, space_name,
                                 oz_page, op_container, tmp_memory, option,
                                 description)
    elif client_lower == 'rest':
        assert_archive_in_op_rest(user, users, hosts, host, space_name,
                                  item_name, spaces, tmp_memory, option,
                                  description)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) removes archive with'
               ' description: "(?P<description>.*)" for item'
               ' "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
               'in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_archive_in_op(client, user, item_name, space_name, host, tmp_memory,
                         selenium, oz_page, op_container, users, hosts,
                         modals, description):
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_archive_in_op_gui(user, selenium, item_name, space_name,
                                 oz_page, op_container, tmp_memory, modals,
                                 description)
    elif client_lower == 'rest':
        remove_archive_in_op_rest(user, users, hosts, host,
                                  description, tmp_memory)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) sees (?P<option>.*) '
               'archive with description: "(?P<description>.*)" for dataset '
               'for item "(?P<item_name>.*)" in space '
               '"(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_with_option_in_op(client, user, item_name, space_name, host,
                                     option, selenium, oz_page, op_container,
                                     tmp_memory, users, hosts, description):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_bagit_archive_in_op_gui(user, selenium, oz_page, space_name,
                                       op_container, tmp_memory, item_name,
                                       option, description)
    elif client_lower == 'rest':
        assert_bagit_archive_in_op_rest(user, users, hosts, host, option,
                                        tmp_memory, description)
    else:
        raise NoSuchClientException(f'Client: {client} not found')

