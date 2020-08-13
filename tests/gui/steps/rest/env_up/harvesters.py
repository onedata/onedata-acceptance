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
    http_post, get_zone_rest_path, http_get, http_delete, http_put)


@wt('user of browser debugger')
def debuggging():
    import pdb
    pdb.set_trace()

@given(parsers.re('using REST, user (?P<user>.*) creates '
                  '(?P<harvesters_list>.*) harvesters? in "(?P<service>.*)" '
                  'Onezone service'))
@given(parsers.re('user (?P<user>.*) has (?P<harvesters_list>.*) harvesters? '
                  'in "(?P<service>.*)" Onezone service'))
def create_harvesters_rest(user, harvesters_list, service, hosts, users,
                           harvesters):
    zone_hostname = hosts[service]['hostname']
    owner = users[user]
    plugin = 'elasticsearch_plugin'
    endpoint = f'{hosts["elasticsearch"]["ip"]}:{ELASTICSEARCH_PORT}'

    for harvester in parse_seq(harvesters_list):
        _create_harvester(zone_hostname, owner.username, owner.password,
                          harvester, endpoint, plugin, harvesters)


def _create_harvester(zone_hostname, owner_username, owner_password,
                      harvester_name, endpoint, plugin, harvesters):
    harvester_details = {'name': harvester_name, 'endpoint': endpoint,
                         'plugin': plugin}
    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'harvesters'),
                         auth=(owner_username, owner_password),
                         data=json.dumps(harvester_details))

    # set harvester id
    harvesters[harvester_name] = response.headers['Location'].split('/')[-1]

    _create_harvester_gui_index(zone_hostname, owner_username, owner_password,
                                harvesters[harvester_name])


def _create_harvester_gui_index(zone_hostname, owner_username, owner_password,
                                harvester_id):
    index_details = {'name': 'generic-index', 'guiPluginName': 'generic-index'}
    http_post(ip=zone_hostname, port=OZ_REST_PORT,
              path=get_zone_rest_path('harvesters', harvester_id, 'indices'),
              auth=(owner_username, owner_password),
              data=json.dumps(index_details))


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


@given(parsers.re('spaces? (?P<space_list>.*) belongs? to '
                  '"(?P<harvester_name>.*)" harvester of user '
                  '(?P<username>.*)'))
def add_space_to_harvester(space_list, harvester_name, spaces, harvesters,
                           hosts, username, users):
    for space in parse_seq(space_list):
        _add_space_to_harvester(space, harvester_name, spaces, harvesters,
                                hosts, username, users)


def _add_space_to_harvester(space_name, harvester_name, spaces, harvesters,
                            hosts, username, users):
    space_id = spaces[space_name]
    harvester_id = harvesters[harvester_name]
    zone_hostname = hosts['onezone']['hostname']

    http_put(ip=zone_hostname, port=OZ_REST_PORT,
             path=get_zone_rest_path('harvesters', harvester_id, 'spaces',
                                     space_id),
             auth=(username, users[username].password))