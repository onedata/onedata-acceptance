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
from tests.utils.rest_utils import (http_post, get_zone_rest_path, http_put)


@given(parsers.parse('initial inventories configuration in "{zone_name}" '
                     'Onezone service:\n{config}'))
def inventories_creation(config, admin_credentials, hosts,
                         users, groups, zone_name, inventories):
    """Create and configure inventories according to given config.

    Config format given in yaml is as follows:

        inventory_name_1:
            owner: user_name

            [users]:                        ---> optional
                - user_name_2
                - user_name_3:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
            [groups]:                       ---> optional
                - group_name_1:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
                - group_name_2
        inventory_name_2:
            ...

    Example configuration:

        inventory1:
            owner: user1
            users:
                - user2
                - user3
            groups:
                - group1
        inventory2:
            owner: user2
    """
    _inventories_creation(config, hosts, users, zone_name, admin_credentials,
                          groups, inventories)


def _inventories_creation(config, hosts, users, zone_name, admin_credentials,
                          groups, inventories):
    zone_hostname = hosts[zone_name]['hostname']
    config = yaml.load(config, yaml.Loader)

    for inventory_name, description in config.items():
        owner = users[description['owner']]

        inventory_id = _create_inventory(zone_hostname, owner, inventory_name)
        inventories[inventory_name] = inventory_id
        for user in description.get('users', {}):
            try:
                [(user, options)] = user.items()
            except AttributeError:
                privileges = None
            else:
                privileges = options['privileges']

            _add_user_to_inventory(zone_hostname, admin_credentials,
                                   inventory_id, users[user].user_id, privileges)

        for group in description.get('groups', {}):
            try:
                [(group, options)] = group.items()
            except AttributeError:
                privileges = None
            else:
                privileges = options['privileges']

            group_id = groups[group]

            _add_group_to_inventory(zone_hostname, admin_credentials,
                                    inventory_id, group_id, privileges)


def _create_inventory(zone_hostname, owner, inventory_name):
    inventory_properties = json.dumps({'name': inventory_name})

    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'atm_inventories'),
                         auth=(owner.username, owner.password),
                         data=inventory_properties)

    return response.headers['location'].split('/')[-1]


def _add_user_to_inventory(zone_hostname, admin_credentials,
                           inventory_id, user_id, privileges):
    if privileges:
        data = json.dumps({'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('atm_inventories', inventory_id, 'users',
                                     user_id),
             auth=(admin_credentials.username, admin_credentials.password),
             data=data)


def _add_group_to_inventory(zone_hostname, admin_credentials, inventory_id,
                            group_id, privileges):
    if privileges:
        data = json.dumps({'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('atm_inventories', inventory_id,
                                     'groups', group_id),
             auth=(admin_credentials.username, admin_credentials.password),
             data=data)

