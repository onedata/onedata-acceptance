"""Steps for inventories creation using REST API.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json

import yaml

from tests import OZ_REST_PORT
from tests.utils.bdd_utils import given, parsers
from tests.utils.rest_utils import (http_post, get_zone_rest_path)


@given(parsers.parse('initial inventories configuration in "{zone_name}" '
                     'Onezone service:\n{config}'))
def inventories_creation(config, hosts, users, zone_name):
    """Create and configure inventories according to given config.

    Config format given in yaml is as follow:

        inventory_name_1:
            owner: user_name
            [users]:                        ---> optional
                - user_name_2
        inventory_name_2:
            ...

    Example configuration:

        inventory1:
            owner: user3
        inventory2:
            owner: user1
            users:
                - user2
                - user3
    """
    _inventories_creation(config, hosts, users, zone_name)


def _inventories_creation(config, hosts, users, zone_name):
    zone_hostname = hosts[zone_name]['hostname']

    config = yaml.load(config)

    for inventory_name, description in config.items():
        owner = users[description['owner']]

        inventory_id = _create_inventory(hosts, zone_hostname, owner.username,
                                         owner.password, inventory_name)
        # inventories[inventory_name] = inventory_id

        for user in description.get('users', {}):
            try:
                [(user, options)] = user.items()
            except AttributeError:
                privileges = None
            else:
                privileges = options['privileges']


def _create_inventory(hosts, zone_name, owner_username, owner_password,
                      inventory_name):
    zone_hostname = hosts[zone_name]['hostname']
    inventory_properties = json.dumps({'name': inventory_name})

    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'atm_inventories'),
                         auth=(owner_username, owner_password),
                         data=inventory_properties)

    return response.headers['location'].split('/')[-1]
