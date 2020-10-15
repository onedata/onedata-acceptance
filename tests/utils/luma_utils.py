"""This module provides utility functions for adding luma mappings"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import hashlib
import json

from tests.utils.rest_utils import get_panel_rest_path, http_post, http_put, http_get
from tests.utils.http_exceptions import HTTPConflict
from tests import PANEL_REST_PORT


def add_user_luma_mapping(admin_user, user, storages):
    # generate uid the same way as it was generated when user was created on storage
    # (see scripts.utils.k8s.pods.create_gusers in one-env-engine)
    uid = int(hashlib.sha1(user.username.encode('utf-8')).hexdigest(), 16) % 50000 + 10000
    for provider_ip, storage_id in storages:
        mapping = {
            'onedataUser': {
                'mappingScheme': 'onedataUser',
                'onedataUserId': user.id
            },
            'storageUser': {
                'storageCredentials': {
                    'uid': uid,
                    'type': 'posix'
                }
            }
        }
        add_mapping(admin_user, provider_ip, storage_id, mapping, http_post,
                    '/'.join(['all', 'onedata_user_to_credentials']))


def add_spaces_luma_mapping(admin_user, storages, spaces):
    storages_ids = [x for _, x in storages]
    for provider_ip, space_id, space_name, storage_id in spaces:
        if storage_id not in storages_ids:
            continue
        # generate gid the same way as it was generated when group was created on storage
        # (see scripts.utils.k8s.pods.create_groups in one-env-engine)
        gid = int(hashlib.sha1(space_name.encode('utf-8')).hexdigest(), 16) % 50000 + 10000
        mapping = {
            'gid': gid
        }
        add_mapping(admin_user, provider_ip, storage_id, mapping, http_put,
                    '/'.join(['posix_compatible', 'default_credentials', space_id]))


def get_local_feed_luma_storages(admin_user, hosts):
    providers_ips = get_providers_ips(hosts)

    storages = []
    for provider_ip in providers_ips:
        response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'storages'),
                            headers={'X-Auth-Token': admin_user.token})
        storages += [(provider_ip, s) for s in json.loads(response.content)['ids']]

    def is_luma_storage(storage_details):
        provider_ip, storage_id = storage_details
        response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'storages', storage_id),
                            headers={'X-Auth-Token': admin_user.token})
        return 'local' == json.loads(response.content)['lumaFeed']

    return [x for x in storages if is_luma_storage(x)]


def get_all_spaces_details(admin_user, hosts):
    providers_ips = get_providers_ips(hosts)

    spaces = []
    for provider_ip in providers_ips:
        response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'spaces'),
                            headers={'X-Auth-Token': admin_user.token})
        spaces += [(provider_ip, s) for s in json.loads(response.content)['ids']]

    def get_space_details(space_info):
        provider_ip, space_id = space_info
        response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'spaces', space_id),
                            headers={'X-Auth-Token': admin_user.token})
        decoded_response = json.loads(response.content)
        return provider_ip, space_id, decoded_response['name'], decoded_response['storageId']

    return [get_space_details(x) for x in spaces]


def get_providers_ips(hosts):
    providers_ips = []
    for service in hosts.values():
        if 'service-type' in service.keys() and service['service-type'] == "oneprovider":
            providers_ips.append(service['ip'])
    return providers_ips


def add_mapping(admin_user, provider_ip, storage_id, mapping, method, path_suffix):
    try:
        response = method(ip=provider_ip, port=PANEL_REST_PORT,
                          path=get_panel_rest_path('provider', 'storages', storage_id, 'luma',
                                                   'local_feed', 'storage_access', path_suffix),
                          data=json.dumps(mapping),
                          headers={
                              'X-Auth-Token': admin_user.token,
                              'Content-Type': 'application/json'
                          })
        assert 204 == response.status_code
    except HTTPConflict:
        # luma mapping for this entity was already added
        pass
