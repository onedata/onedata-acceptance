"""Steps for groups creation using REST API.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json

import yaml

from tests import OZ_REST_PORT
from tests.utils.bdd_utils import given, parsers
from tests.utils.rest_utils import (
    http_post, http_put, get_zone_rest_path, http_get, http_delete)
from tests.utils.http_exceptions import HTTPForbidden


@given(parsers.parse('initial groups configuration in "{service}" '
                     'Onezone service:\n{config}'))
def groups_creation(config, service, admin_credentials,
                    users, hosts, groups):
    """Create and configure groups according to given config.

    Config format given in yaml is as follow:

        group_name_1:
            owner: user_name
            [users]:                        ---> optional
                - user_name_2
                - user_name_3:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
            [groups]:                       ---> optional
                - child_group_1             
                - child_group_2:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
        group_name_2:
            ...

    Example configuration:

        group1:
            owner: user3
        group2:
            owner: user1
            users:
                - user2:
                    privileges:
                        - group_invite_user
                        - group_remove_user
                - user3
            groups:
                - group1:
                    privileges:
                        - group_view
                        - group_invite_user
                - group3
        group3:
            owner: user2
    """
    _groups_creation(config, service, admin_credentials,
                     users, hosts, groups)


def _groups_creation(config, service, admin_credentials,
                     users, hosts, groups):
    zone_hostname = hosts[service]['hostname']

    config = yaml.load(config)

    for group_name, description in config.items():
        owner = users[description['owner']]

        group_id = _create_group(zone_hostname, owner.username,
                                 owner.password, group_name)
        groups[group_name] = group_id

        for user in description.get('users', {}):
            try:
                [(user, options)] = user.items()
            except AttributeError:
                privileges = None
            else:
                privileges = options['privileges']

            _add_user_to_group(zone_hostname, admin_credentials,
                               group_id, users[user].id, privileges)

    for group_name, description in config.items():
        group_id = groups[group_name]
        for child_group in description.get('groups', {}):
            try:
                [(child_group, options)] = child_group.items()
            except AttributeError:
                privileges = None
            else:
                privileges = options['privileges']

            child_id = groups[child_group]

            _add_child_group(zone_hostname, admin_credentials, group_id, 
                             child_id, privileges)


def _create_group(zone_hostname, owner_username, owner_password,
                  group_name, group_type='team'):
    group_properties = {'name': group_name, 'type': group_type}
    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'groups'),
                         auth=(owner_username, owner_password),
                         data=json.dumps(group_properties))
    return response.headers['location'].split('/')[-1]


def _add_user_to_group(zone_hostname, admin_credentials,
                       group_id, user_id, privileges):
    if privileges:
        data = json.dumps({'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('groups', group_id, 'users', user_id),
             auth=(admin_credentials.username, admin_credentials.password),
             data=data)


def _add_child_group(zone_hostname, admin_credentials, parent_id, child_id, 
                     privileges):
    if privileges:
        data = json.dumps({'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('groups', parent_id, 'children', child_id),
             auth=(admin_credentials.username, admin_credentials.password),
             data=data)


def _get_group_id(hosts, users, user, group_name):
    service = 'onezone'
    zone_hostname = hosts[service]['hostname']
    groups_id_list = get_group_id_list(user, users, zone_hostname)
    for group_id in groups_id_list:
        group_details = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                                 path=get_zone_rest_path('groups', group_id),
                                 auth=(user, users[user].password))
        if group_details.json()['name'] == group_name:
            return group_id
    return None


@given(parsers.parse('there is no {group_name} group in Onezone page used by '
                     '{user} before definition in next steps'))
def remove_group_in_onezone(hosts, users, user, group_name):
    service = 'onezone'
    zone_hostname = hosts[service]['hostname']
    group_id = _get_group_id(hosts, users, user, group_name)
    if group_id:
        http_delete(ip=zone_hostname, port=OZ_REST_PORT,
                    path=get_zone_rest_path('groups', group_id),
                    auth=(user, users[user].password))


@given(parsers.parse('there is no groups in Onezone page used by {user} before '
                     'definition in next steps'))
def remove_all_groups_rest(user, hosts, users):
    zone_hostname = hosts['onezone']['hostname']

    groups_id_list = get_group_id_list(user, users, zone_hostname)

    for group in groups_id_list:
        _try_to_remove_group(group, zone_hostname, user, users)


def _try_to_remove_group(group_id, zone_hostname, user, users):
    try:
        http_delete(ip=zone_hostname, port=OZ_REST_PORT,
                    path=get_zone_rest_path('groups', group_id),
                    auth=(user, users[user].password))
    except HTTPForbidden:
        pass


def get_group_id_list(user, users, zone_hostname):
    groups_list = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                           path=get_zone_rest_path('groups'),
                           auth=(user, users[user].password))
    return groups_list.json()['groups']

