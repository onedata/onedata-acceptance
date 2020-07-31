"""Steps for spaces creation using REST API.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
import yaml
import json

from pytest_bdd import given, parsers

from tests import OZ_REST_PORT, PANEL_REST_PORT, OP_REST_PORT
from tests.utils.rest_utils import (http_get, http_post, http_put,
                                    get_panel_rest_path, get_zone_rest_path,
                                    get_provider_rest_path, http_delete)
from tests.utils.http_exceptions import HTTPNotFound, HTTPError, HTTPBadRequest
from tests.utils.utils import repeat_failed


@given(parsers.parse('initial spaces configuration in "{zone_host}" '
                     'Onezone service:\n{config}'))
def create_and_configure_spaces(config, zone_host, admin_credentials,
                                onepanel_credentials, hosts,
                                users, groups, storages, spaces):
    """Create and configure spaces according to given config.

    Config format given in yaml is as follow:

        space_name_1:
            owner: user_name                ---> currently we identify user account with concrete
                                                 browser so user_name == browser_id
            [users]:                        ---> optional
                - user_name_2
                - user_name_3:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
            [home space for]:               ---> optional
                - user_name_1
                - user_name_2
            [groups]:                       ---> optional
                - group_name_1:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
                - group_name_2
            [providers]:                    ---> optional
                - provider_name_1:
                    storage: name
                    size: size in bits
            [storage]:                      ---> optional
                defaults:
                    provider: provider_name         --> default provider on whose storage
                                                        files will be created
                directory tree:
                    - dir0                  ---> name starting with 'dir' prefix
                                                 is treated as directory
                    - dir2:
                        - file0: text
                        - file1:
                            provider: p2    ---> mandatory if dict form is used
                            content: text
                        - file2

        space_name_2:
            ...

    Example configuration:

        space1:
            owner: user1
            users:
                - user2
                - user3
            home space for:
                - user1
            groups:
                - group1
            providers:
                - p1:
                    storage: onestorage
                    size: 1000000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1
                    - dir2:
                        - file0
                        - file1: 11111
                        - file2:
                            provider: 2
                            content: 22222
    """
    _create_and_configure_spaces(config, zone_host, admin_credentials,
                                 onepanel_credentials, hosts,
                                 users, groups, storages, spaces)


@given(parsers.parse('additional spaces configuration in "{zone_host}" '
                     'Onezone service:\n{config}'))
def add_spaces_configuration(config, zone_host, admin_credentials,
                             onepanel_credentials, hosts,
                             users, groups, storages, spaces):
    _create_and_configure_spaces(config, zone_host, admin_credentials,
                                 onepanel_credentials, hosts, users, groups,
                                 storages, spaces)


def _create_and_configure_spaces(config, zone_name, admin_credentials,
                                 onepanel_credentials, hosts,
                                 users_db, groups_db, storages_db, spaces_db):
    zone_hostname = hosts[zone_name]['hostname']

    for space_name, description in yaml.load(config).items():
        owner = users_db[description['owner']]
        users_to_add = description.get('users', [])
        spaces_db[space_name] = space_id = _create_space(zone_hostname,
                                                         owner.username,
                                                         owner.password,
                                                         space_name)
        _add_users_to_space(zone_hostname, admin_credentials, space_id,
                            users_db, users_to_add)
        _add_groups_to_space(zone_hostname, admin_credentials, space_id,
                             groups_db, description.get('groups', {}))
        _get_support(zone_hostname, onepanel_credentials, owner, space_id,
                     storages_db, hosts, description.get('providers', {}),
                     users_to_add, users_db)
        _init_storage_from_config(owner, space_name, hosts,
                                  description.get('storage', {}))


def _create_space(zone_hostname, owner_username, owner_password, space_name):
    space_properties = {'name': space_name}
    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'spaces'),
                         auth=(owner_username, owner_password),
                         data=json.dumps(space_properties))
    return response.headers['location'].split('/')[-1]


def _add_users_to_space(zone_hostname, admin_credentials, space_id,
                        users_db, users_to_add):
    for user in users_to_add:
        try:
            [(user, options)] = user.items()
        except AttributeError:
            privileges = None
        else:
            privileges = options['privileges']

        _add_user_to_space(zone_hostname, admin_credentials.username,
                           admin_credentials.password, space_id,
                           users_db[user].id, privileges)


def _add_user_to_space(zone_hostname, admin_username, admin_password,
                       space_id, user_id, privileges):
    if privileges:
        data = json.dumps({'operation': 'set',
                           'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('spaces', space_id, 'users', user_id),
             auth=(admin_username, admin_password), data=data)


def _add_groups_to_space(zone_hostname, admin_credentials, space_id,
                         groups_db, groups_to_add):
    for group in groups_to_add:
        try:
            [(group, options)] = group.items()
        except AttributeError:
            privileges = None
        else:
            privileges = options['privileges']

        _add_group_to_space(zone_hostname, admin_credentials.username,
                            admin_credentials.password, space_id,
                            groups_db[group], privileges)


def _add_group_to_space(zone_hostname, admin_username, admin_password,
                        space_id, group_id, privileges):
    if privileges:
        data = json.dumps({'operation': 'set',
                           'privileges': privileges})
    else:
        data = None

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('spaces', space_id, 'groups', group_id),
             auth=(admin_username, admin_password), data=data)


def _get_support(zone_hostname, onepanel_credentials,
                 owner_credentials, space_id, storages_db, hosts, providers,
                 members, users):
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    for provider in providers:
        [(provider, options)] = provider.items()

        provider_name = hosts[provider]['name']
        provider_hostname = hosts[provider]['hostname']
        storage_name = options['storage']

        if provider_name not in storages_db:
            storages_db[provider_name] = {}

        try:
            storage_id = storages_db[provider_name][storage_name]
        except KeyError:
            storage_id = storages_db[provider_name][storage_name] = \
                _get_storage_id(provider_hostname, onepanel_username,
                                onepanel_password, storage_name)

        token = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                          path=get_zone_rest_path('spaces', space_id,
                                                  'providers', 'token'),
                          auth=(owner_credentials.username,
                                owner_credentials.password)).json()['token']

        space_support_details = {'token': token,
                                 'size': int(options['size']),
                                 'storageId': storage_id}
        http_post(ip=provider_hostname, port=PANEL_REST_PORT,
                  path=get_panel_rest_path('provider', 'spaces'),
                  auth=(onepanel_username, onepanel_password),
                  data=json.dumps(space_support_details))

        all_members = [owner_credentials.username] + members
        wait_for_space_support(space_id, provider_hostname, all_members, users)


@repeat_failed(attempts=10, interval=0.5,
               exceptions=(AssertionError, HTTPError))
def wait_for_space_support(space_id, provider_hostname, members, users):
    for user in members:
        response = http_get(ip=provider_hostname, port=OP_REST_PORT,
                            path=get_provider_rest_path('spaces'),
                            headers={'X-Auth-Token': users[user].token}).content
        space_id_list = [space['spaceId'] for space in json.loads(response)]

        assert space_id in space_id_list, ('space {} not found in user '
                                           '{} spaces'.format(space_id,
                                                              user))


def _get_storage_id(provider_hostname, onepanel_username,
                    onepanel_password, storage_name):
    storages_id = http_get(ip=provider_hostname, port=PANEL_REST_PORT,
                           path=get_panel_rest_path('provider', 'storages'),
                           auth=(onepanel_username, onepanel_password))
    for storage_id in storages_id.json()['ids']:
        storage_details = http_get(ip=provider_hostname, port=PANEL_REST_PORT,
                                   path=get_panel_rest_path('provider',
                                                            'storages',
                                                            storage_id),
                                   auth=(onepanel_username, onepanel_password))
        if storage_details.json()['name'] == storage_name:
            return storage_id


def _init_storage_from_config(owner_credentials, space_name, hosts,
                              storage_conf):
    if not storage_conf:
        return

    defaults = storage_conf['defaults']
    provider_hostname = hosts[defaults['provider']]['hostname']
    directory_tree = storage_conf['directory tree']

    init_storage(owner_credentials, space_name, hosts,
                 provider_hostname, directory_tree)


def init_storage(owner_credentials, space_name, hosts,
                 provider_hostname, directory_tree):
    # if we make call to fast after deleting users from previous test
    # provider cache was not refreshed and call will create dir for
    # now nonexistent user, to avoid this wait some time
    import time
    time.sleep(2)

    def create_cdmi_object(path, data=None, repeats=10, auth=None,
                           headers={'X-Auth-Token': owner_credentials.token}):
        response = None
        for _ in range(repeats):
            try:
                response = http_put(ip=provider_hostname, port=OP_REST_PORT,
                                    path='/cdmi/' + path, headers=headers, 
                                    auth=auth, data=data)
            except (HTTPNotFound, HTTPBadRequest, HTTPError):
                # because user may not yet exist in provider first call
                # will fail, as such wait some time and try again
                time.sleep(1)
            else:
                break

        return response

    _mkdirs(create_cdmi_object, space_name, hosts, directory_tree)


def _mkdirs(create_cdmi_obj, cwd, hosts, dir_content=None):
    if not dir_content:
        return

    for item in dir_content:
        try:
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None

        path = cwd + '/' + name
        if name.startswith('dir'):
            create_cdmi_obj(path + '/')
            _mkdirs(create_cdmi_obj, path, hosts, content)
        else:
            _mkfile(create_cdmi_obj, path, hosts, content)


def _mkfile(create_cdmi_obj, file_path, hosts, file_content=None):
    if file_content:
        try:
            provider = file_content['provider']
        except TypeError:
            create_cdmi_obj(file_path, str(file_content))
        else:
            create_cdmi_obj(file_path, data=file_content.get('content', None),
                            url='https://{}:{}/cdmi/'.format(hosts[provider]['hostname'],
                                                             OP_REST_PORT))
    else:
        create_cdmi_obj(file_path)


def _get_users_space_id_list(zone_hostname, owner_username, owner_password):

    resp = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                    path=get_zone_rest_path('user', 'spaces'),
                    auth=(owner_username, owner_password)).json()
    spaces_id_list = resp['spaces']
    return spaces_id_list


def _rm_all_spaces_for_user(zone_hostname, owner_username, owner_password):
    spaces_id_list = _get_users_space_id_list(zone_hostname, owner_username,
                                              owner_password)

    for space_id in spaces_id_list:
        http_delete(ip=zone_hostname, port=OZ_REST_PORT,
                    path=get_zone_rest_path('spaces', space_id),
                    auth=(owner_username, owner_password))


def _rm_all_spaces_for_users_list(zone_hostname, users_db):
    for user_credentials in users_db.values():
        _rm_all_spaces_for_user(zone_hostname, user_credentials.username,
                                user_credentials.password)


