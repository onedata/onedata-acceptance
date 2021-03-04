"""This module contains gherkin steps for operations on LUMA.
"""

__author__ = "Michal Stanisz, Natalia Organek"
__copyright__ = "Copyright (C) 2018-2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import json

import yaml

from tests import PANEL_REST_PORT
from tests.gui.meta_steps.onepanel.storages import get_first_storage_id_by_name
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import parsers, wt
from tests.utils.rest_utils import (
    http_put, http_post, get_panel_rest_path)


@wt(parsers.parse('LUMA local feed mappings are created with following '
                  'configuration:\n{config}'))
def wt_create_luma_mappings(config, users, spaces, hosts,
                            onepanel_credentials):
    """ Create LUMA mappings according to given config.

            Config format given in yaml is as follow:

            provider_name:
              storage_name:
                type: storage_type
                users:                                   --> optional
                  user_name:
                    storage uid: uid
                    display uid: uid                     --> optional
                  ...
                spaces:                                  --> optional
                  space_name:
                    space POSIX storage defaults: gid
                    space display defaults: gid         --> optional
                  ...
              ...
            ...
        """
    _wt_create_luma_mappings(config, users, spaces, hosts, onepanel_credentials)


def _wt_create_luma_mappings(config, users, spaces, hosts,
                             onepanel_credentials):
    mappings = yaml.load(config)
    for provider in mappings:
        storages = mappings[provider]
        for storage in storages:
            storage_mappings = storages[storage]
            storage_type = storage_mappings['type']
            storage_id = get_first_storage_id_by_name(storage, provider, hosts,
                                                      onepanel_credentials)
            user_mappings = storage_mappings.get('users', [])
            for user in user_mappings:
                user_data = user_mappings[user]
                storage_uid = user_data.get('storage uid')
                display_uid = user_data.get('display uid')
                set_user_luma_local_feed_mappings(provider, hosts, users,
                                                  onepanel_credentials,
                                                  storage_id, storage_type,
                                                  user, storage_uid,
                                                  display_uid)
            space_mappings = storage_mappings.get('spaces', [])
            for space in space_mappings:
                space_data = space_mappings[space]
                default_gid = space_data.get('space POSIX storage defaults')
                display_gid = space_data.get('space display defaults')
                set_default_posix_credentials_luma_lf(provider, storage_id,
                                                      space, hosts,
                                                      onepanel_credentials,
                                                      spaces, default_gid)
                if display_gid:
                    set_default_display_credentials_luma_lf(provider,
                                                            storage_id,
                                                            space, hosts,
                                                            onepanel_credentials,
                                                            spaces, display_gid)


def set_user_luma_local_feed_mappings(provider, hosts, users,
                                      onepanel_credentials,
                                      storage_id, storage_type, user,
                                      storage_uid, display_uid):
    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password
    user_id = users[user].id
    mapping_scheme = _set_onedata_user_mapping(storage_type, user_id,
                                               storage_uid, display_uid)

    http_post(ip=provider_hostname, port=PANEL_REST_PORT,
              path=get_panel_rest_path('provider', 'storages', storage_id,
                                       'luma', 'local_feed',
                                       'storage_access', 'all',
                                       'onedata_user_to_credentials'),
              data=json.dumps(mapping_scheme),
              auth=(onepanel_username, onepanel_password))


def _set_onedata_user_mapping(storage_type, user_id, storage_uid, display_uid):
    scheme = {
        'onedataUser': {
            'mappingScheme': 'onedataUser',
            'onedataUserId': user_id
        },
        'storageUser': {
            'storageCredentials': {
                'type': storage_type,
                'uid': storage_uid,
            }
        }
    }
    if display_uid:
        scheme['storageUser']['displayUid'] = display_uid
    return scheme


def set_default_posix_credentials_luma_lf(provider, storage_id, space, hosts,
                                          onepanel_credentials, spaces,
                                          default_gid):
    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password
    mapping_scheme = {'gid': int(default_gid)}
    space_id = spaces[space]
    http_put(ip=provider_hostname, port=PANEL_REST_PORT,
             path=get_panel_rest_path('provider', 'storages', storage_id,
                                      'luma', 'local_feed',
                                      'storage_access', 'posix_compatible',
                                      'default_credentials', space_id),
             data=json.dumps(mapping_scheme),
             auth=(onepanel_username, onepanel_password))


def set_default_display_credentials_luma_lf(provider, storage_id, space, hosts,
                                            onepanel_credentials, spaces,
                                            display_gid):
    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password
    mapping_scheme = {'gid': int(display_gid)}
    space_id = spaces[space]
    http_put(ip=provider_hostname, port=PANEL_REST_PORT,
             path=get_panel_rest_path('provider', 'storages', storage_id,
                                      'luma', 'local_feed',
                                      'display_credentials', 'all', 'default',
                                      space_id),
             data=json.dumps(mapping_scheme),
             auth=(onepanel_username, onepanel_password))


@wt(parsers.parse('LUMA local feed mappings for imported storage "{storage}" '
                  'at "{provider}" are created between '
                  '{uid_list} and {user_list}'))
def create_imported_storage_luma_mappings_lf(storage, provider, uid_list,
                                             user_list, hosts,
                                             onepanel_credentials, users):
    uids = parse_seq(uid_list)
    users_list = parse_seq(user_list)
    storage_id = get_first_storage_id_by_name(storage, provider, hosts,
                                              onepanel_credentials)

    mappings = zip(uids, users_list)
    for uid, user in mappings:
        _insert_mapping_of_uid_into_lf(uid, user, provider, hosts,
                                       onepanel_credentials, storage_id, users)


def _insert_mapping_of_uid_into_lf(uid, user, provider, hosts,
                                   onepanel_credentials,
                                   storage_id, users):
    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password
    mapping_scheme = {'mappingScheme': 'onedataUser',
                      'onedataUserId': str(users[user].id)}

    http_put(ip=provider_hostname, port=PANEL_REST_PORT,
             path=get_panel_rest_path('provider', 'storages', storage_id,
                                      'luma', 'local_feed', 'storage_import',
                                      'posix_compatible',
                                      'uid_to_onedata_user', uid),
             data=json.dumps(mapping_scheme),
             auth=(onepanel_username, onepanel_password))
