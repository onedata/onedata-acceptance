"""This module contains gherkin steps to run mixed acceptance tests featuring
datasets using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.dataset import *
from tests.mixed.steps.rest.oneprovider.data import create_dataset_in_op_rest
from tests.mixed.utils.common import NoSuchClientException


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) creates dataset '
               '(?P<option>.*)for item "(?P<item_name>.*)" in space '
               '"(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset_in_op(client, user, item_name, space_name, host, tmp_memory,
                         selenium, oz_page, op_container, modals, users, hosts,
                         option):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_dataset(user, tmp_memory, item_name, space_name,
                       selenium, oz_page, op_container, modals, option=option)
    elif client_lower == 'rest':
        create_dataset_in_op_rest(user, users, hosts, host, space_name,
                                  item_name, option)
    else:
        raise NoSuchClientException(f'Client: {client} not found')

