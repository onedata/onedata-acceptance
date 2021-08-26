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
def inventories_creation(config, hosts, users, groups, zone_name):
    """Create and configure inventories according to given config.

    Config format given in yaml is as follow:

        inventory_name_1:
            owner: user_name
            [users]:                        ---> optional
                - user_name_2
                - user_name_3
            [groups]:                       ---> optional
                - group_name_1

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
    _create_and_configure_inventories(config, hosts, users, zone_name, users,
                                      groups)


def _create_and_configure_inventories(config, hosts, users, zone_name):
    zone_hostname = hosts[zone_name]['hostname']

    config = yaml.load(config)

    for inventory_name, description in config.items():
        owner = users[description['owner']]
        users_to_add = description.get('users', [])

        inventory_id = _create_inventory(zone_hostname, owner.username,
                                         owner.password,
                                         inventory_name)

        _add_users_to_inventory(zone_hostname, admin_credentials, inventory_id,
                                users_db, users_to_add)
        _add_groups_to_inventory(zone_hostname, admin_credentials, inventory_id,
                                 groups_db, description.get('groups', {}))


def _create_inventory(zone_hostname, owner_username, owner_password,
                      inventory_name):
    inventory_properties = json.dumps({'name': inventory_name})

    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'atm_inventories'),
                         auth=(owner_username, owner_password),
                         data=inventory_properties)

    return response.headers['location'].split('/')[-1]


def _add_users_to_inventory(zone_hostname, admin_credentials, inventory_id,
                            users_db, users_to_add):
    for user in users_to_add:
        try:
            [(user, options)] = user.items()
        except AttributeError:
            privileges = None
        else:
            privileges = options['privileges']

        _add_user_to_inventory(zone_hostname, admin_credentials.username,
                               admin_credentials.password, inventory_id,
                               users_db[user].id, privileges)


def _add_user_to_inventory(zone_hostname, admin_username, admin_password,
                           inventory_id, user_id, privileges):
    if privileges:
        data = json.dumps({'operation': 'set',
                           'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('spaces', inventory_id, 'users', user_id),
             auth=(admin_username, admin_password), data=data)


def _add_groups_to_inventory(zone_hostname, admin_credentials, inventory_id,
                             groups_db, groups_to_add):
    for group in groups_to_add:
        try:
            [(group, options)] = group.items()
        except AttributeError:
            privileges = None
        else:
            privileges = options['privileges']

        _add_group_to_inventory(zone_hostname, admin_credentials.username,
                                admin_credentials.password, inventory_id,
                                groups_db[group], privileges)


def _add_group_to_inventory(zone_hostname, admin_username, admin_password,
                            inventory_id, group_id, privileges):
    if privileges:
        data = json.dumps({'operation': 'set',
                           'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('spaces', inventory_id, 'groups', group_id),
             auth=(admin_username, admin_password), data=data)
