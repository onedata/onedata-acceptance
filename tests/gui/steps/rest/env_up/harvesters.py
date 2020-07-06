"""Steps for harvesters management using REST API.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json

from tests import OZ_REST_PORT, ELASTICSEARCH_PORT
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt, parsers, given
from tests.utils.rest_utils import (
    http_post, get_zone_rest_path, http_get, http_delete)


@given(parsers.re('using REST, user (?P<user>.*) creates '
                  '(?P<harvesters_list>.*) harvesters? in "(?P<service>.*)" '
                  'Onezone service'))
def create_harvesters_rest(user, harvesters_list, service, hosts, users):
    zone_hostname = hosts[service]['hostname']
    owner = users[user]
    plugin = 'elasticsearch_plugin'
    endpoint = f'{hosts["elasticsearch"]["ip"]}:{ELASTICSEARCH_PORT}'

    for harvester in parse_seq(harvesters_list):
        _create_harvester(zone_hostname, owner.username, owner.password,
                          harvester, endpoint, plugin)


def _create_harvester(zone_hostname, owner_username, owner_password,
                      harvester_name, endpoint, plugin):
    harvester_details = {'name': harvester_name, 'endpoint': endpoint,
                         'plugin': plugin}
    http_post(ip=zone_hostname, port=OZ_REST_PORT,
              path=get_zone_rest_path('user', 'harvesters'),
              auth=(owner_username, owner_password),
              data=json.dumps(harvester_details))


@given(parsers.parse('user {user} has no harvesters'))
def remove_all_harvesters_rest(user, hosts, users):
    zone_hostname = hosts['onezone']['hostname']

    dict_harvesters = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                               path=get_zone_rest_path('user', 'harvesters'),
                               auth=(user, users[user].password)).json()
    list_harvesters = dict_harvesters['harvesters']

    for harvester in list_harvesters:
        _remove_harvester(harvester, zone_hostname, user, users)


def _remove_harvester(harvester_id, zone_hostname, user, users):
    http_delete(ip=zone_hostname, port=OZ_REST_PORT,
                path=get_zone_rest_path('harvesters', harvester_id),
                auth=(user, users[user].password))
