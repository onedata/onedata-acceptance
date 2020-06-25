"""Steps for shares management using REST API.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json

from tests import OP_REST_PORT
from tests.utils.bdd_utils import wt, given, parsers
from tests.utils.rest_utils import http_get, get_provider_rest_path, http_post


@given(parsers.parse('using REST, user {user} creates "{share_name}" share of '
                     '"{item_path}" supported by "{provider}" provider'))
def create_share_rest(item_path, provider, user, share_name, hosts, users):
    provider_hostname = hosts[provider]['hostname']
    file_id = get_file_id_by_rest(item_path, provider_hostname, user, users)
    print(file_id)

    share_details = {'name': share_name, 'fileId': file_id}

    http_post(ip=provider_hostname, port=OP_REST_PORT,
              path=get_provider_rest_path('shares'),
              headers={'X-Auth-Token': users[user].token},
              data=json.dumps(share_details))


def get_file_id_by_rest(file_path, provider_hostname, user, users):
    response = http_post(ip=provider_hostname, port=OP_REST_PORT,
                         path=get_provider_rest_path('lookup-file-id',
                                                     file_path),
                         headers={'X-Auth-Token': users[user].token}).content
    return json.loads(response)['fileId']
