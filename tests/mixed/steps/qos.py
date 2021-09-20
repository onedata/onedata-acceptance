"""This module contains gherkin steps to run mixed acceptance tests featuring
quality of service using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.qos import *
from tests.mixed.steps.rest.oneprovider.data import *


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) creates '
               '"(?P<expression>.*)" QoS requirement for "(?P<file_name>.*)" in'
               ' space "(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_qos_requirement_in_op(client, user, selenium, modals, file_name,
                                 tmp_memory, expression, oz_page, op_container,
                                 popups, space_name, users, hosts, host):
    client_lower = client.lower()
    if client_lower == 'web gui':
        add_qos_requirement_in_modal(selenium, user, modals, file_name,
                                     tmp_memory, expression, oz_page,
                                     op_container, popups, space_name)
    elif client_lower == 'rest':
        create_qos_requirement_in_op_rest(user, users, hosts, host, expression,
                                          space_name, file_name)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that file '
               '"(?P<file_name>.*)" (?P<option>has not|has some) QoS '
               'requirements in space "(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_qos_file_status_in_op(client, user, file_name, space_name, host,
                                 tmp_memory, selenium, oz_page, op_container,
                                 users, hosts, option):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_qos_file_status_in_op_gui(user, file_name, space_name,
                                         tmp_memory, selenium, oz_page,
                                         op_container, option)
    elif client_lower == 'rest':
        assert_qos_file_status_in_op_rest(user, users, hosts, host,
                                          space_name, file_name, option)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) deletes all QoS '
               'requirements for "(?P<file_name>.*)" in space '
               '"(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_qos_requirement_in_op(client, selenium, user, space_name, oz_page,
                                 modals, popups, file_name, tmp_memory,
                                 op_container, users, hosts, host):
    client_lower = client.lower()
    if client_lower == 'web gui':
        delete_qos_requirement_in_op_gui(selenium, user, space_name, oz_page,
                                         modals, popups, file_name, tmp_memory,
                                         op_container)
    elif client_lower == 'rest':
        delete_qos_requirement_in_op_rest(user, users, hosts, host, space_name,
                                          file_name)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


