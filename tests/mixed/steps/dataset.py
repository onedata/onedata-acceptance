"""This module contains gherkin steps to run mixed acceptance tests featuring
datasets using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")
from tests.gui.meta_steps.oneprovider.dataset import *
from tests.mixed.oneprovider_client.api.dataset_api import DatasetApi
from tests.mixed.utils.common import NoSuchClientException, login_to_provider


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) creates dataset for item'
               ' "(?P<item_name>.*)"  in space "(?P<space_name>.*)" '
               'in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset_in_op(client, user, item_name, space_name, host, tmp_memory,
                         selenium, oz_page, op_container, modals, users, hosts):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_dataset(user, tmp_memory, item_name, space_name,
                       selenium, oz_page, op_container, modals)

    elif client_lower == 'rest':
        path = f'{space_name}/{item_name}'
        client = login_to_provider(user, users, hosts[host]['hostname'])
        dataset_api = DatasetApi(client)
    else:
        raise NoSuchClientException(f'Client: {client} not found')
