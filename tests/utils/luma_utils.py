"""This module provides utility functions for adding luma mappings"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import hashlib
import json
from collections import namedtuple
from typing import Union, Dict, List, Any

from tests.utils.rest_utils import get_panel_rest_path, http_post, http_put, http_get
from tests.utils.http_exceptions import HTTPConflict
from tests import PANEL_REST_PORT
from tests.utils.user_utils import AdminUser, User

SpaceDetails = namedtuple("SpaceDetails", ['space_id', 'provider_ip', 'space_name', 'storage_id'])
StorageDetails = namedtuple("StorageDetails", ['storage_id', 'provider_ip'])


def add_user_luma_mapping(
        admin_user: AdminUser,
        user: User,
        storages: List[StorageDetails]
) -> None:

    # generate uid the same way as it was generated when user was created on storage
    # (see scripts.utils.k8s.pods.create_users in one-env-engine)
    uid = int(hashlib.sha1(user.username.encode('utf-8')).hexdigest(), 16) % 50000 + 10000
    for storage_details in storages:
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
        add_mapping(admin_user, storage_details.provider_ip, storage_details.storage_id,
                    mapping, http_post, '/'.join(['all', 'onedata_user_to_credentials']))


def add_spaces_luma_mapping(
        admin_user: AdminUser,
        storages: List[StorageDetails],
        spaces_details: List[SpaceDetails]
) -> None:

    storages_ids = [x for _, x in storages]
    for space_details in spaces_details:
        if space_details.storage_id not in storages_ids:
            continue
        # generate gid the same way as it was generated when group was created on storage
        # (see scripts.utils.k8s.pods.create_groups in one-env-engine)
        gid = int(hashlib.sha1(space_details.space_name.encode('utf-8')).
                  hexdigest(), 16) % 50000 + 10000
        mapping = {
            'gid': gid
        }
        add_mapping(admin_user, space_details.provider_ip,
                    space_details.storage_id, mapping, http_put,
                    '/'.join(['posix_compatible', 'default_credentials',
                              space_details. space_id]))


def get_local_feed_luma_storages(
        admin_user: AdminUser,
        hosts: Dict[str, Any]
) -> List[StorageDetails]:

    providers_ips = get_providers_ips(hosts)
    storages = []
    for provider_ip in providers_ips:
        response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'storages'),
                            headers={'X-Auth-Token': admin_user.token})

        for storage_id in json.loads(response.content)['ids']:
            response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                                path=get_panel_rest_path('provider', 'storages', storage_id),
                                headers={'X-Auth-Token': admin_user.token})
            loaded_response = json.loads(response.content)
            if 'lumaFeed' in loaded_response and 'local' == loaded_response['lumaFeed']:
                storages.append(StorageDetails(storage_id, provider_ip))

    return storages


def get_all_spaces_details(admin_user: AdminUser, hosts: Dict[str, Any]) -> List[SpaceDetails]:
    providers_ips = get_providers_ips(hosts)
    spaces_details = []
    for provider_ip in providers_ips:
        response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'spaces'),
                            headers={'X-Auth-Token': admin_user.token})

        for space_id in json.loads(response.content)['ids']:
            response = http_get(ip=provider_ip, port=PANEL_REST_PORT,
                                path=get_panel_rest_path('provider', 'spaces', space_id),
                                headers={'X-Auth-Token': admin_user.token})
            decoded_response = json.loads(response.content)
            spaces_details.append(SpaceDetails(space_id, provider_ip, decoded_response['name'],
                                               decoded_response['storageId']))

    return spaces_details


def get_providers_ips(hosts: Dict[str, Any]) -> List[str]:
    providers_ips = []
    for service in hosts.values():
        if 'service-type' in service.keys() and service['service-type'] == "oneprovider":
            providers_ips.append(service['ip'])
    return providers_ips


def add_mapping(
        admin_user: AdminUser,
        provider_ip: str,
        storage_id: str,
        mapping: Dict[str, Union[Dict[str, str], int]],
        method: Union[http_post, http_put],
        path_suffix: str
) -> None:

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
