"""Steps for shares management using REST API.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests import OP_REST_PORT
from tests.utils.rest_utils import get_provider_rest_path, http_get


def get_provider_id(provider, hosts, users):
    user = 'admin'
    provider_hostname = hosts[provider]['hostname']
    provider_conf = http_get(ip=provider_hostname, port=OP_REST_PORT,
                             path=get_provider_rest_path('configuration'),
                             auth=(user, users[user].password)).json()
    return provider_conf['providerId']
