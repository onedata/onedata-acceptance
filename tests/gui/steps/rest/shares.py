"""Steps for shares management using REST API.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json

import yaml

from tests import OP_REST_PORT, OZ_REST_PORT
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.rest_utils import (get_provider_rest_path, http_post,
                                    http_get, get_zone_rest_path, http_put)


@given(parsers.parse('using REST, user {user} creates "{share_name}" share of '
                     '"{item_path}" supported by "{provider}" provider'))
def create_share_using_rest(item_path, provider, user, share_name, hosts,
                            users):
    provider_hostname = hosts[provider]['hostname']
    file_id = get_file_id_by_rest(item_path, provider_hostname, user, users)

    share_details = {'name': share_name, 'fileId': file_id}

    http_post(ip=provider_hostname, port=OP_REST_PORT,
              path=get_provider_rest_path('shares'),
              headers={'X-Auth-Token': users[user].token},
              data=json.dumps(share_details))


@wt(parsers.parse('using REST, user {user} creates "{share_name}" share of '
                  '"{item_path}" supported by "{provider}" provider'))
def wt_create_share_using_rest(item_path, provider, user, share_name, hosts,
                               users):
    create_share_using_rest(item_path, provider, user, share_name, hosts, users)


@given(parsers.parse('using REST, user {user} creates following shares:\n'
                     '{config}'))
def create_many_shares_using_rest(user, config, hosts, users):
    """Config:

        - name: share name
          path: path of file to make share for
          provider: provider that supports space

    """
    _create_many_shares_using_rest(user, config, hosts, users)


def _create_many_shares_using_rest(user, config, hosts, users):
    data = yaml.load(config, yaml.Loader)
    for share in data:
        name = share['name']
        path = share['path']
        provider = share['provider']

        create_share_using_rest(path, provider, user, name, hosts, users)


def get_file_id_by_rest(file_path, provider_hostname, user, users):
    response = http_post(ip=provider_hostname, port=OP_REST_PORT,
                         path=get_provider_rest_path('lookup-file-id',
                                                     file_path),
                         headers={'X-Auth-Token': users[user].token}).content
    return json.loads(response)['fileId']


@given(parsers.parse('user {user} is added to mock handle service in {host}'))
def add_user_to_handle_service(user, users, host, hosts):
    zone_hostname = hosts[transform(host)]['hostname']
    handle_service_id = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                                 path=get_zone_rest_path('handle_services'),
                                 headers={'X-Auth-Token': users['admin'].token}
                                 ).json()['handle_services'][0]
    http_put(ip=zone_hostname, port=OZ_REST_PORT, path=get_zone_rest_path(
        'handle_services', handle_service_id, 'users', users[user].user_id),
             headers={'X-Auth-Token': users['admin'].token})


